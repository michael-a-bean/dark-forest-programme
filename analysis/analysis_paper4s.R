#!/usr/bin/env Rscript
# =============================================================================
# analysis_r3.R -- Publication figures for Paper 4S (Revision 3)
#
# Covers the complete experimental programme: Exps F, B, 7b, S, E/E2, R2,
# 17/17np, 5/5np.  Generates Figures 1-9.
#
# Usage:  cd papers/04s-bounds && Rscript analysis_r3.R
# =============================================================================

library(arrow)
library(dplyr)
library(tidyr)
library(ggplot2)
library(patchwork)

theme_set(theme_minimal(base_size = 11))

# --- Paths -------------------------------------------------------------------
bounds_data  <- file.path(dirname(dirname(getwd())), "data")
meta_data    <- normalizePath("~/research/dark-forest-metaplastic/data")
fig_dir      <- file.path(getwd(), "figures")
dir.create(fig_dir, showWarnings = FALSE)

read_bounds <- function(name) {
  path <- file.path(bounds_data, name, "session_metrics.parquet")
  if (file.exists(path)) read_parquet(path) else { warning(paste("Missing:", name)); NULL }
}
read_meta <- function(name) {
  path <- file.path(meta_data, name, "session_metrics.parquet")
  if (file.exists(path)) read_parquet(path) else { warning(paste("Missing:", name)); NULL }
}

save_fig <- function(name, plot, w, h) {
  ggsave(file.path(fig_dir, paste0(name, ".pdf")), plot, width = w, height = h)
  ggsave(file.path(fig_dir, paste0(name, ".png")), plot, width = w, height = h, dpi = 300)
  cat("  Saved", name, "\n")
}

# --- Style conventions -------------------------------------------------------
# Committee decision: DROP sigmoid (tanh == sigmoid). Show only hard, tanh, oja.
bound_colours <- c("hard" = "#E63946", "tanh" = "#457B9D", "oja" = "#E9C46A")
bound_labels  <- c("hard" = "Hard clip", "tanh" = "Tanh", "oja" = "Oja")
bound_order   <- c("hard", "tanh", "oja")

drop_sigmoid <- function(df, col = "bound_type") {
  df |> filter(.data[[col]] != "sigmoid")
}


# =============================================================================
# Fig 1: Disordinal interaction (Exp F)
# =============================================================================
cat("=== Fig 1: Disordinal interaction (Exp F) ===\n")

dF <- read_bounds("expF_factorial")
if (!is.null(dF)) {
  dF_final <- dF |>
    filter(session == max(session)) |>
    drop_sigmoid() |>
    mutate(
      pruning = ifelse(prune_on, "Pruned", "No pruning"),
      bound_type = factor(bound_type, levels = bound_order)
    ) |>
    group_by(bound_type, pruning) |>
    summarise(
      n_asm = mean(n_assemblages),
      se    = sd(n_assemblages) / sqrt(n()),
      .groups = "drop"
    )

  fig1 <- ggplot(dF_final, aes(x = bound_type, y = n_asm, fill = pruning)) +
    geom_col(position = position_dodge(0.8), width = 0.7, alpha = 0.85) +
    geom_errorbar(aes(ymin = n_asm - se, ymax = n_asm + se),
                  position = position_dodge(0.8), width = 0.2) +
    scale_x_discrete(labels = bound_labels) +
    scale_fill_manual(values = c("Pruned" = "#264653", "No pruning" = "#A8DADC")) +
    labs(x = "Weight bound", y = "Assemblage count (final session)",
         fill = NULL,
         title = "Fig 1. Disordinal interaction: pruning reverses bound-type ranking") +
    theme(legend.position = "bottom")

  save_fig("fig1_disordinal_interaction", fig1, 7, 5)
}


# =============================================================================
# Fig 2: Pruning threshold sweep (Exp B)
# =============================================================================
cat("=== Fig 2: Pruning threshold sweep (Exp B) ===\n")

dB <- read_bounds("expB_prune_sweep")
if (!is.null(dB)) {
  dB_final <- dB |>
    filter(session == max(session)) |>
    drop_sigmoid() |>
    mutate(bound_type = factor(bound_type, levels = bound_order)) |>
    group_by(bound_type, prune_threshold) |>
    summarise(
      n_asm = mean(n_assemblages),
      se    = sd(n_assemblages) / sqrt(n()),
      .groups = "drop"
    )

  fig2 <- ggplot(dB_final, aes(x = prune_threshold, y = n_asm,
                                colour = bound_type, shape = bound_type)) +
    geom_line(linewidth = 0.8) +
    geom_point(size = 2.5) +
    geom_errorbar(aes(ymin = n_asm - se, ymax = n_asm + se), width = 0.15) +
    scale_x_log10(breaks = unique(dB_final$prune_threshold),
                  labels = scales::label_scientific()) +
    scale_colour_manual(values = bound_colours, labels = bound_labels) +
    scale_shape_manual(values = c("hard" = 16, "tanh" = 17, "oja" = 15),
                       labels = bound_labels) +
    labs(x = "Pruning threshold (log scale)",
         y = "Assemblage count (final session)",
         colour = NULL, shape = NULL,
         title = "Fig 2. Threshold sweep: soft bounds show cliff between 1e-6 and 1e-5") +
    theme(legend.position = "bottom", panel.grid.minor = element_blank())

  save_fig("fig2_threshold_sweep", fig2, 8, 5)
}


# =============================================================================
# Fig 3: Steepness non-monotonicity (Exp 7b, baseline from 2b)
# =============================================================================
cat("=== Fig 3: Steepness non-monotonicity (Exp 7b) ===\n")

d7b <- read_bounds("exp7b_steepness_noprune")
d2b <- read_bounds("exp2b_baseline_noprune")

if (!is.null(d7b)) {
  d7b_final <- d7b |>
    filter(session == max(session)) |>
    group_by(steepness) |>
    summarise(
      n_asm = mean(n_assemblages),
      se    = sd(n_assemblages) / sqrt(n()),
      .groups = "drop"
    )

  # Baseline horizontal lines from exp2b (no-prune, each bound type)
  base_lines <- NULL
  if (!is.null(d2b)) {
    base_lines <- d2b |>
      filter(session == max(session), locality == 0.10) |>
      drop_sigmoid() |>
      group_by(bound_type) |>
      summarise(n_asm = mean(n_assemblages), .groups = "drop")
  }

  # Hard clip as a separate point at x position beyond max steepness
  hard_x <- max(d7b_final$steepness) * 2  # place hard clip marker at 100

  fig3 <- ggplot(d7b_final, aes(x = steepness, y = n_asm)) +
    geom_line(linewidth = 0.8, colour = "#457B9D") +
    geom_point(size = 2.5, colour = "#457B9D") +
    geom_errorbar(aes(ymin = n_asm - se, ymax = n_asm + se),
                  width = 0.08, colour = "#457B9D")

  if (!is.null(base_lines)) {
    for (i in seq_len(nrow(base_lines))) {
      bt <- base_lines$bound_type[i]
      fig3 <- fig3 +
        geom_hline(yintercept = base_lines$n_asm[i],
                   linetype = "dashed", colour = bound_colours[bt], alpha = 0.7) +
        annotate("text", x = min(d7b_final$steepness),
                 y = base_lines$n_asm[i] + 0.3,
                 label = paste0(bound_labels[bt], " (no prune)"),
                 colour = bound_colours[bt], hjust = 0, size = 3)
    }
  }

  fig3 <- fig3 +
    scale_x_log10(breaks = c(1, 2, 3, 5, 10, 20, 50),
                  labels = c("1", "2", "3", "5", "10", "20", "50")) +
    labs(x = "Steepness k (log scale)",
         y = "Assemblage count (final session, no pruning)",
         title = "Fig 3. Steepness non-monotonicity without pruning") +
    theme(panel.grid.minor = element_blank())

  save_fig("fig3_steepness_nonmonotone", fig3, 8, 5)
}


# =============================================================================
# Fig 4: Steepness mechanism (Exp S) - 4-panel
# =============================================================================
cat("=== Fig 4: Steepness mechanism (Exp S) ===\n")

dS <- read_bounds("expS_steepness_eta")
if (!is.null(dS)) {
  dS_final <- dS |>
    filter(session == max(session)) |>
    group_by(steepness) |>
    summarise(
      n_asm         = mean(n_assemblages),
      se_asm        = sd(n_assemblages) / sqrt(n()),
      mean_weight   = mean(mean_weight),
      se_weight     = sd(mean_weight) / sqrt(n()),
      pct_saturated = mean(pct_saturated),
      se_sat        = sd(pct_saturated) / sqrt(n()),
      act_mean      = mean(act_mean),
      se_act        = sd(act_mean) / sqrt(n()),
      .groups = "drop"
    )

  common_theme <- theme(panel.grid.minor = element_blank())
  kcolor <- "#2A9D8F"

  fig4a <- ggplot(dS_final, aes(x = steepness, y = n_asm)) +
    geom_line(linewidth = 0.8, colour = kcolor) +
    geom_point(size = 2, colour = kcolor) +
    geom_errorbar(aes(ymin = n_asm - se_asm, ymax = n_asm + se_asm),
                  width = 0.08, colour = kcolor) +
    scale_x_log10() +
    labs(x = "k", y = "Assemblages", title = "A. Assemblage count") +
    common_theme

  fig4b <- ggplot(dS_final, aes(x = steepness, y = mean_weight)) +
    geom_line(linewidth = 0.8, colour = kcolor) +
    geom_point(size = 2, colour = kcolor) +
    geom_errorbar(aes(ymin = mean_weight - se_weight, ymax = mean_weight + se_weight),
                  width = 0.08, colour = kcolor) +
    scale_x_log10() +
    labs(x = "k", y = "Mean |weight|", title = "B. Mean weight") +
    common_theme

  fig4c <- ggplot(dS_final, aes(x = steepness, y = pct_saturated)) +
    geom_line(linewidth = 0.8, colour = kcolor) +
    geom_point(size = 2, colour = kcolor) +
    geom_errorbar(aes(ymin = pct_saturated - se_sat, ymax = pct_saturated + se_sat),
                  width = 0.08, colour = kcolor) +
    scale_x_log10() +
    labs(x = "k", y = "% saturated", title = "C. Weight saturation") +
    common_theme

  fig4d <- ggplot(dS_final, aes(x = steepness, y = act_mean)) +
    geom_line(linewidth = 0.8, colour = kcolor) +
    geom_point(size = 2, colour = kcolor) +
    geom_errorbar(aes(ymin = act_mean - se_act, ymax = act_mean + se_act),
                  width = 0.08, colour = kcolor) +
    scale_x_log10() +
    labs(x = "k", y = "Mean activity", title = "D. Mean activity") +
    common_theme

  fig4 <- (fig4a | fig4b) / (fig4c | fig4d) +
    plot_annotation(title = "Fig 4. Steepness mechanism: sharp transition at k ~ 1.5")

  save_fig("fig4_steepness_mechanism", fig4, 10, 7)
}


# =============================================================================
# Fig 5: Eta F-ratio comparison (Exp E + E2)
# =============================================================================
cat("=== Fig 5: Eta F-ratio (Exp E + E2) ===\n")

dE  <- read_bounds("expE_eta_snapshots")
dE2 <- read_bounds("expE2_eta_extended")

if (!is.null(dE)) {
  # From expE: all 4 weight bounds under soft eta, final observations with F-ratio
  eE_soft <- dE |>
    filter(eta_bound_type == "soft", !is.na(eta_f_ratio)) |>
    drop_sigmoid(col = "weight_bound_type") |>
    group_by(weight_bound_type) |>
    summarise(
      f_mean = mean(eta_f_ratio),
      f_se   = sd(eta_f_ratio) / sqrt(n()),
      n_obs  = n(),
      .groups = "drop"
    ) |>
    rename(bound_type = weight_bound_type)

  # Supplement with expE2 (extended hard-only run, more seeds)
  if (!is.null(dE2)) {
    eE2_hard <- dE2 |>
      filter(session == max(session), !is.na(eta_f_ratio)) |>
      summarise(
        f_mean = mean(eta_f_ratio),
        f_se   = sd(eta_f_ratio) / sqrt(n()),
        n_obs  = n()
      ) |>
      mutate(bound_type = "hard")

    # Use the better-powered E2 estimate for hard
    eE_soft <- eE_soft |>
      filter(bound_type != "hard") |>
      bind_rows(eE2_hard)
  }

  eE_soft <- eE_soft |>
    mutate(bound_type = factor(bound_type, levels = bound_order))

  fig5 <- ggplot(eE_soft, aes(x = bound_type, y = f_mean, fill = bound_type)) +
    geom_col(width = 0.6, alpha = 0.85) +
    geom_errorbar(aes(ymin = f_mean - f_se, ymax = f_mean + f_se), width = 0.2) +
    geom_hline(yintercept = 1.0, linetype = "dashed", colour = "grey40") +
    annotate("text", x = 0.6, y = 1.15, label = "F = 1.0 (no differentiation)",
             hjust = 0, size = 3, colour = "grey40") +
    scale_x_discrete(labels = bound_labels) +
    scale_fill_manual(values = bound_colours, guide = "none") +
    labs(x = "Weight bound", y = "Eta F-ratio (between / within assemblage variance)",
         title = "Fig 5. Only hard clip enables eta differentiation under soft eta bounds") +
    theme(panel.grid.minor = element_blank())

  save_fig("fig5_eta_fratio", fig5, 6, 5)
}


# =============================================================================
# Fig 6: Deconfounded probes (Exp R2)
# =============================================================================
cat("=== Fig 6: Deconfounded probes (Exp R2) ===\n")

dR2 <- read_bounds("expR2_deconfounded_probes")
if (!is.null(dR2)) {
  dR2_long <- dR2 |>
    drop_sigmoid() |>
    filter(!is.na(uniform_mean_js)) |>
    mutate(
      pruning = ifelse(prune_on, "Pruned", "No pruning"),
      bound_type = factor(bound_type, levels = bound_order)
    ) |>
    select(bound_type, pruning, seed,
           uniform_mean_js, uniform_response_rank,
           gaussian_mean_js, gaussian_response_rank) |>
    pivot_longer(cols = c(uniform_mean_js, uniform_response_rank,
                          gaussian_mean_js, gaussian_response_rank),
                 names_to = "metric_raw", values_to = "value") |>
    mutate(
      probe_type = ifelse(grepl("uniform", metric_raw), "Uniform", "Gaussian"),
      metric     = ifelse(grepl("js", metric_raw), "JS divergence", "Response rank")
    )

  dR2_summary <- dR2_long |>
    filter(!is.na(value)) |>
    group_by(bound_type, pruning, probe_type, metric) |>
    summarise(
      mean_val = mean(value),
      se       = sd(value) / sqrt(n()),
      .groups = "drop"
    )

  fig6 <- ggplot(dR2_summary,
                 aes(x = bound_type, y = mean_val, fill = pruning)) +
    geom_col(position = position_dodge(0.8), width = 0.7, alpha = 0.85) +
    geom_errorbar(aes(ymin = mean_val - se, ymax = mean_val + se),
                  position = position_dodge(0.8), width = 0.2) +
    facet_grid(metric ~ probe_type, scales = "free_y") +
    scale_x_discrete(labels = bound_labels) +
    scale_fill_manual(values = c("Pruned" = "#264653", "No pruning" = "#A8DADC")) +
    labs(x = "Weight bound", y = NULL, fill = NULL,
         title = "Fig 6. Spatial deconfounding: Gaussian probes inflate JS, deflate rank") +
    theme(legend.position = "bottom")

  save_fig("fig6_deconfounded_probes", fig6, 10, 7)
}


# =============================================================================
# Fig 7: No-pruning response rank (Exp 17np vs 17)
# =============================================================================
cat("=== Fig 7: Response rank (Exp 17 vs 17np) ===\n")

d17   <- read_meta("exp17_response_matrix")
d17np <- read_meta("exp17np_response_noprune")

if (!is.null(d17) && !is.null(d17np)) {
  combo17 <- bind_rows(
    d17   |> mutate(pruning = "Pruned (original)"),
    d17np |> mutate(pruning = "No pruning")
  )

  combo17_summary <- combo17 |>
    group_by(condition, pruning) |>
    summarise(
      mean_rank = mean(response_rank),
      se        = sd(response_rank) / sqrt(n()),
      .groups   = "drop"
    ) |>
    mutate(condition = factor(condition,
                              levels = c("baseline", "global_target",
                                         "local_hard", "local_soft")))

  fig7 <- ggplot(combo17_summary,
                 aes(x = condition, y = mean_rank, fill = pruning)) +
    geom_col(position = position_dodge(0.8), width = 0.7, alpha = 0.85) +
    geom_errorbar(aes(ymin = mean_rank - se, ymax = mean_rank + se),
                  position = position_dodge(0.8), width = 0.2) +
    scale_fill_manual(values = c("Pruned (original)" = "#264653",
                                 "No pruning" = "#A8DADC")) +
    labs(x = "Condition", y = "Response rank",
         fill = NULL,
         title = "Fig 7. Removing pruning dramatically increases response rank") +
    theme(legend.position = "bottom")

  save_fig("fig7_response_rank", fig7, 8, 5)
}


# =============================================================================
# Fig 8: Parameter landscape transformation (Exp 5np vs 5)
# =============================================================================
cat("=== Fig 8: Parameter landscape (Exp 5 vs 5np) ===\n")

d5   <- read_meta("exp5_corrective")
d5np <- read_meta("exp5np_corrective_noprune")

if (!is.null(d5) && !is.null(d5np)) {
  # Original (pruned): final session, aggregate over seeds
  d5_heat <- d5 |>
    filter(session == max(session), meta_strength > 0, inhibitor_coupling >= 0) |>
    group_by(meta_strength, inhibitor_coupling) |>
    summarise(n_asm = mean(n_assemblages), .groups = "drop") |>
    mutate(regime = "Pruned (original)")

  d5np_heat <- d5np |>
    filter(session == max(session), meta_strength > 0, inhibitor_coupling >= 0) |>
    group_by(meta_strength, inhibitor_coupling) |>
    summarise(n_asm = mean(n_assemblages), .groups = "drop") |>
    mutate(regime = "No pruning")

  heat_data <- bind_rows(d5_heat, d5np_heat) |>
    mutate(regime = factor(regime, levels = c("Pruned (original)", "No pruning")))

  # Shared colour range
  zrange <- range(heat_data$n_asm, na.rm = TRUE)

  fig8 <- ggplot(heat_data,
                 aes(x = factor(meta_strength), y = factor(inhibitor_coupling),
                     fill = n_asm)) +
    geom_tile(colour = "white", linewidth = 0.3) +
    facet_wrap(~ regime) +
    scale_fill_viridis_c(option = "inferno", limits = zrange,
                         name = "Assemblages") +
    labs(x = "Meta-strength", y = "Inhibitor coupling",
         title = "Fig 8. Removing pruning opens the parameter landscape") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          panel.grid = element_blank())

  save_fig("fig8_parameter_landscape", fig8, 11, 5)
}


# =============================================================================
# Fig 9: Three regimes summary
# =============================================================================
cat("=== Fig 9: Three regimes summary ===\n")

# Collect representative metrics for each regime:
#   Topological = hard clip, pruned (exp F pruned condition)
#   Structural  = tanh, pruned (exp F pruned condition)
#   Metaplastic = hard clip, no-prune with meta (exp 17np local_soft or exp E2)

regime_data <- NULL

if (!is.null(dF)) {
  topo <- dF |>
    filter(session == max(session), bound_type == "hard", prune_on == TRUE) |>
    summarise(
      n_asm = mean(n_assemblages),
      .groups = "drop"
    ) |> mutate(regime = "Topological")

  struct <- dF |>
    filter(session == max(session), bound_type == "tanh", prune_on == TRUE) |>
    summarise(
      n_asm = mean(n_assemblages),
      .groups = "drop"
    ) |> mutate(regime = "Structural")

  meta_asm <- dF |>
    filter(session == max(session), bound_type == "hard", prune_on == FALSE) |>
    summarise(n_asm = mean(n_assemblages)) |> pull(n_asm)

  regime_data <- bind_rows(topo, struct,
                            tibble(n_asm = meta_asm, regime = "Metaplastic"))
}

# Response rank from exp17 / 17np
rr_topo <- rr_struct <- rr_meta <- NA
if (!is.null(d17)) {
  # Topological: baseline (hard clip, pruned original)
  rr_topo <- d17 |> filter(condition == "local_hard") |>
    summarise(rr = mean(response_rank)) |> pull(rr)
  rr_struct <- d17 |> filter(condition == "local_soft") |>
    summarise(rr = mean(response_rank)) |> pull(rr)
}
if (!is.null(d17np)) {
  rr_meta <- d17np |> filter(condition == "local_soft") |>
    summarise(rr = mean(response_rank)) |> pull(rr)
}

# F-ratio: hard from E2, tanh from E, oja from E
fr_topo <- fr_struct <- fr_meta <- NA
if (!is.null(dE2)) {
  fr_meta <- dE2 |> filter(session == max(session), !is.na(eta_f_ratio)) |>
    summarise(f = mean(eta_f_ratio)) |> pull(f)
}
if (!is.null(dE)) {
  # Topological regime uses hard eta -- no differentiation by design
  fr_topo <- 0
  fr_struct <- dE |>
    filter(eta_bound_type == "soft", weight_bound_type == "tanh", !is.na(eta_f_ratio)) |>
    summarise(f = mean(eta_f_ratio)) |> pull(f)
}

summary_tbl <- tibble(
  Regime           = c("Topological", "Structural", "Metaplastic"),
  `Assemblages`    = if (!is.null(regime_data)) regime_data$n_asm else rep(NA, 3),
  `Response rank`  = c(rr_topo, rr_struct, rr_meta),
  `Eta F-ratio`    = c(fr_topo, fr_struct, fr_meta)
)

cat("\nThree-regime summary table:\n")
print(summary_tbl)

# Render as a figure using a bar chart grouped by metric
summary_long <- summary_tbl |>
  pivot_longer(cols = -Regime, names_to = "Metric", values_to = "Value") |>
  mutate(Regime = factor(Regime, levels = c("Topological", "Structural", "Metaplastic")))

regime_colours <- c("Topological" = "#E63946", "Structural" = "#457B9D",
                    "Metaplastic" = "#2A9D8F")

fig9 <- ggplot(summary_long, aes(x = Regime, y = Value, fill = Regime)) +
  geom_col(width = 0.6, alpha = 0.85) +
  facet_wrap(~ Metric, scales = "free_y") +
  scale_fill_manual(values = regime_colours, guide = "none") +
  labs(x = NULL, y = NULL,
       title = "Fig 9. Three regimes: topological, structural, and metaplastic") +
  theme(panel.grid.minor = element_blank())

save_fig("fig9_three_regimes", fig9, 10, 4)


cat("\n=== All R3 figures complete ===\n")
