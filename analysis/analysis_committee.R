#!/usr/bin/env Rscript
# Committee-requested analyses: formation dynamics, Mann-Whitney tests,
# pruning control comparison, CCD permutation results, steepness sweep.
#
# Run AFTER cluster_job_committee.py completes and data is copied locally.
# Usage: cd papers/04s-bounds && Rscript analysis_committee.R

library(arrow)
library(dplyr)
library(tidyr)
library(ggplot2)
library(patchwork)

theme_set(theme_minimal(base_size = 11))
data_dir <- file.path(dirname(dirname(getwd())), "data")
fig_dir <- file.path(getwd(), "figures")
dir.create(fig_dir, showWarnings = FALSE)

bound_colours <- c("hard"="#E63946", "tanh"="#457B9D", "sigmoid"="#2A9D8F", "oja"="#E9C46A")
bound_labels <- c("hard"="Hard clip", "tanh"="Tanh", "sigmoid"="Sigmoid", "oja"="Oja")

read_exp <- function(name) {
  path <- file.path(data_dir, name, "session_metrics.parquet")
  if (file.exists(path)) read_parquet(path) else { warning(paste("Missing:", name)); NULL }
}

# ============================================================
# 1. Formation dynamics (from existing Exp 2 data)
# ============================================================
cat("=== Formation dynamics ===\n")

d2 <- read_exp("exp2_coexistence")
if (!is.null(d2)) {
  d2_traj <- d2 |>
    filter(locality == 0.10) |>
    group_by(bound_type, session) |>
    summarise(
      n_asm = mean(n_assemblages),
      n_asm_se = sd(n_assemblages) / sqrt(n()),
      ccd = mean(centroid_cosine_distance),
      n_edges = mean(n_edges),
      mean_weight = mean(mean_weight),
      .groups = "drop"
    )

  fig_fd_a <- ggplot(d2_traj, aes(x = session, y = n_asm, colour = bound_type)) +
    geom_line(linewidth = 0.8) +
    geom_ribbon(aes(ymin = n_asm - n_asm_se, ymax = n_asm + n_asm_se,
                    fill = bound_type), alpha = 0.15, colour = NA) +
    scale_colour_manual(values = bound_colours, labels = bound_labels) +
    scale_fill_manual(values = bound_colours, labels = bound_labels) +
    labs(x = "Session", y = "Assemblages", title = "A. Assemblage count over time (locality=0.10)") +
    theme(legend.position = "bottom")

  fig_fd_b <- ggplot(d2_traj, aes(x = session, y = n_edges, colour = bound_type)) +
    geom_line(linewidth = 0.8) +
    scale_colour_manual(values = bound_colours, labels = bound_labels) +
    labs(x = "Session", y = "Edge count", title = "B. Edge survival") +
    theme(legend.position = "bottom")

  fig_fd_c <- ggplot(d2_traj, aes(x = session, y = mean_weight, colour = bound_type)) +
    geom_line(linewidth = 0.8) +
    scale_colour_manual(values = bound_colours, labels = bound_labels) +
    labs(x = "Session", y = "Mean |weight|", title = "C. Weight accumulation") +
    theme(legend.position = "bottom")

  fig_fd <- fig_fd_a + fig_fd_b + fig_fd_c +
    plot_layout(guides = "collect") & theme(legend.position = "bottom")
  ggsave(file.path(fig_dir, "fig9_formation_dynamics.pdf"), fig_fd, width = 14, height = 4)
  ggsave(file.path(fig_dir, "fig9_formation_dynamics.png"), fig_fd, width = 14, height = 4, dpi = 300)
  cat("  Saved fig9_formation_dynamics\n")
}

# ============================================================
# 2. Mann-Whitney U tests
# ============================================================
cat("\n=== Mann-Whitney U tests ===\n")

if (!is.null(d2)) {
  final2 <- d2 |> filter(session == max(session))

  cat("\nExp 2: n_assemblages at locality=0.10, final session\n")
  for (bt in c("tanh", "sigmoid", "oja")) {
    hard_vals <- final2 |> filter(bound_type == "hard", locality == 0.10) |> pull(n_assemblages)
    other_vals <- final2 |> filter(bound_type == bt, locality == 0.10) |> pull(n_assemblages)
    test <- wilcox.test(hard_vals, other_vals, alternative = "two.sided", exact = FALSE)
    effect_r <- 1 - 2 * test$statistic / (length(hard_vals) * length(other_vals))
    cat(sprintf("  hard vs %s: U=%.0f, p=%.2e, r=%.3f (hard mean=%.1f, %s mean=%.1f)\n",
                bt, test$statistic, test$p.value, effect_r,
                mean(hard_vals), bt, mean(other_vals)))
  }

  cat("\nExp 2: n_assemblages at locality=0.05, final session\n")
  for (bt in c("tanh", "sigmoid", "oja")) {
    hard_vals <- final2 |> filter(bound_type == "hard", locality == 0.05) |> pull(n_assemblages)
    other_vals <- final2 |> filter(bound_type == bt, locality == 0.05) |> pull(n_assemblages)
    test <- wilcox.test(hard_vals, other_vals, alternative = "two.sided", exact = FALSE)
    effect_r <- 1 - 2 * test$statistic / (length(hard_vals) * length(other_vals))
    cat(sprintf("  hard vs %s: U=%.0f, p=%.2e, r=%.3f (hard mean=%.1f, %s mean=%.1f)\n",
                bt, test$statistic, test$p.value, effect_r,
                mean(hard_vals), bt, mean(other_vals)))
  }

  cat("\n  tanh vs sigmoid at locality=0.10:\n")
  tanh_vals <- final2 |> filter(bound_type == "tanh", locality == 0.10) |> pull(n_assemblages)
  sig_vals <- final2 |> filter(bound_type == "sigmoid", locality == 0.10) |> pull(n_assemblages)
  test_ts <- wilcox.test(tanh_vals, sig_vals, exact = FALSE)
  cat(sprintf("  U=%.0f, p=%.4f\n", test_ts$statistic, test_ts$p.value))
}

d4 <- read_exp("exp4_continuous")
if (!is.null(d4)) {
  final4 <- d4 |> filter(session == max(session))

  cat("\nExp 4: CCD, final session\n")
  for (wbt in c("hard", "tanh", "sigmoid", "oja")) {
    hard_eta <- final4 |> filter(weight_bound_type == wbt, eta_bound_type == "hard") |>
      pull(centroid_cosine_distance)
    soft_eta <- final4 |> filter(weight_bound_type == wbt, eta_bound_type == "soft") |>
      pull(centroid_cosine_distance)
    if (length(hard_eta) > 0 && length(soft_eta) > 0 && sd(c(hard_eta, soft_eta)) > 0) {
      test <- wilcox.test(hard_eta, soft_eta, exact = FALSE)
      cat(sprintf("  w=%s: hard_eta CCD=%.3f, soft_eta CCD=%.3f, U=%.0f, p=%.2e\n",
                  wbt, mean(hard_eta), mean(soft_eta), test$statistic, test$p.value))
    } else {
      cat(sprintf("  w=%s: hard_eta CCD=%.3f, soft_eta CCD=%.3f (no variance for test)\n",
                  wbt, mean(hard_eta), mean(soft_eta)))
    }
  }

  cat("\nExp 4: CCD soft eta, hard_w vs tanh_w:\n")
  hw <- final4 |> filter(weight_bound_type == "hard", eta_bound_type == "soft") |>
    pull(centroid_cosine_distance)
  tw <- final4 |> filter(weight_bound_type == "tanh", eta_bound_type == "soft") |>
    pull(centroid_cosine_distance)
  test_hw_tw <- wilcox.test(hw, tw, exact = FALSE)
  cat(sprintf("  U=%.0f, p=%.2e (hard_w mean=%.3f, tanh_w mean=%.3f)\n",
              test_hw_tw$statistic, test_hw_tw$p.value, mean(hw), mean(tw)))
}

# ============================================================
# 3. Pruning control comparison (Exp 2 vs Exp 2a)
# ============================================================
cat("\n=== Pruning control comparison ===\n")

d2a <- read_exp("exp2a_no_pruning")
if (!is.null(d2a) && !is.null(d2)) {
  final2a <- d2a |> filter(session == max(session))
  final2_orig <- d2 |> filter(session == max(session))

  cat("Final session assemblages: original (prune=1e-4) vs no-pruning\n")
  for (bt in c("hard", "tanh", "sigmoid", "oja")) {
    for (loc in c(0.05, 0.10, 0.20)) {
      orig <- final2_orig |> filter(bound_type == bt, abs(locality - loc) < 0.001)
      nop <- final2a |> filter(bound_type == bt, abs(locality - loc) < 0.001)
      cat(sprintf("  %s loc=%.2f: pruned=%.1f+/-%.1f, no_prune=%.1f+/-%.1f, edges: %d vs %d\n",
                  bt, loc,
                  mean(orig$n_assemblages), sd(orig$n_assemblages),
                  mean(nop$n_assemblages), sd(nop$n_assemblages),
                  round(mean(orig$n_edges)), round(mean(nop$n_edges))))
    }
  }

  # Combined comparison figure
  combined <- bind_rows(
    final2_orig |> mutate(pruning = "Standard (1e-4)") |>
      select(bound_type, locality, n_assemblages, pruning),
    final2a |> mutate(pruning = "Disabled") |>
      select(bound_type, locality, n_assemblages, pruning)
  ) |>
    group_by(bound_type, locality, pruning) |>
    summarise(n_asm = mean(n_assemblages), se = sd(n_assemblages)/sqrt(n()), .groups = "drop")

  fig_prune <- ggplot(combined |> filter(locality %in% c(0.05, 0.10, 0.20)),
                       aes(x = bound_type, y = n_asm, fill = pruning)) +
    geom_col(position = position_dodge(0.8), width = 0.7, alpha = 0.8) +
    geom_errorbar(aes(ymin = n_asm - se, ymax = n_asm + se),
                  position = position_dodge(0.8), width = 0.2) +
    facet_wrap(~ paste("locality =", locality)) +
    scale_fill_manual(values = c("Standard (1e-4)" = "#457B9D", "Disabled" = "#E9C46A")) +
    labs(x = "Bound type", y = "Assemblages", fill = "Pruning",
         title = "Effect of pruning threshold on assemblage count") +
    theme(legend.position = "bottom")

  ggsave(file.path(fig_dir, "fig10_pruning_control.pdf"), fig_prune, width = 10, height = 5)
  ggsave(file.path(fig_dir, "fig10_pruning_control.png"), fig_prune, width = 10, height = 5, dpi = 300)
  cat("  Saved fig10_pruning_control\n")
}

# ============================================================
# 4. CCD permutation test results (Exp 6)
# ============================================================
cat("\n=== CCD permutation test results ===\n")

d6 <- read_exp("exp6_ccd_permutation")
if (!is.null(d6)) {
  cat("Per-condition summary:\n")
  d6_summary <- d6 |>
    group_by(weight_bound_type, eta_bound_type) |>
    summarise(
      real_ccd = mean(real_ccd),
      null_mean = mean(null_ccd_mean),
      null_95th = mean(null_ccd_95th),
      mean_p = mean(p_value),
      n_significant = sum(p_value < 0.05),
      n_seeds = n(),
      .groups = "drop"
    )
  print(d6_summary)
}

# ============================================================
# 5. Steepness sweep (Exp 7)
# ============================================================
cat("\n=== Steepness sweep ===\n")

d7 <- read_exp("exp7_steepness")
if (!is.null(d7)) {
  d7_final <- d7 |>
    filter(session == max(session)) |>
    group_by(steepness) |>
    summarise(
      n_asm = mean(n_assemblages),
      n_asm_se = sd(n_assemblages) / sqrt(n()),
      modularity = mean(modularity),
      ccd = mean(centroid_cosine_distance),
      mean_weight = mean(mean_weight),
      n_edges = mean(n_edges),
      .groups = "drop"
    )

  print(d7_final)

  # Add hard clip baseline from Exp 2 at locality=0.10
  hard_baseline <- d2 |>
    filter(session == max(session), bound_type == "hard", abs(locality - 0.10) < 0.001) |>
    summarise(n_asm = mean(n_assemblages), n_asm_se = sd(n_assemblages)/sqrt(n()),
              modularity = mean(modularity), ccd = mean(centroid_cosine_distance),
              mean_weight = mean(mean_weight), n_edges = mean(n_edges)) |>
    mutate(steepness = Inf)

  d7_plot <- bind_rows(d7_final, hard_baseline)

  fig_steep <- ggplot(d7_plot, aes(x = steepness, y = n_asm)) +
    geom_line(linewidth = 0.8, colour = "#457B9D") +
    geom_point(size = 2.5, colour = "#457B9D") +
    geom_errorbar(aes(ymin = n_asm - n_asm_se, ymax = n_asm + n_asm_se),
                  width = 0.1, colour = "#457B9D") +
    scale_x_continuous(trans = "log10",
                       breaks = c(1, 2, 3, 5, 10, 20, 50, Inf),
                       labels = c("1", "2", "3", "5", "10", "20", "50", "hard")) +
    labs(x = "Steepness k (log scale, hard clip at right)",
         y = "Assemblages at session 200",
         title = "Critical steepness for assemblage formation (locality = 0.10)") +
    theme(panel.grid.minor = element_blank())

  ggsave(file.path(fig_dir, "fig11_steepness.pdf"), fig_steep, width = 7, height = 5)
  ggsave(file.path(fig_dir, "fig11_steepness.png"), fig_steep, width = 7, height = 5, dpi = 300)
  cat("  Saved fig11_steepness\n")
}

cat("\n=== All committee analyses complete ===\n")
