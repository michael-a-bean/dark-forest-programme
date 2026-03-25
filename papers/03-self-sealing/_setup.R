# Shared R setup for Paper 3: Differentiation
# Sourced by knitr setup chunk in paper.qmd

library(tidyverse)
library(arrow)
library(ggthemes)
library(viridis)
library(patchwork)
library(scales)

# --- Data access ---
DATA_DIR <- normalizePath(file.path(here::here(), "data"), mustWork = FALSE)

read_experiment <- function(experiment, table = "session_metrics") {
  path <- file.path(DATA_DIR, experiment, paste0(table, ".parquet"))
  read_parquet(path) |> as_tibble()
}

# --- Tufte theme ---
theme_tufte_paper <- function(base_size = 11) {
  theme_tufte(base_size = base_size, base_family = "serif") +
    theme(
      plot.title = element_text(size = base_size + 1, face = "plain", hjust = 0),
      plot.subtitle = element_text(size = base_size - 1, color = "grey40", hjust = 0),
      axis.title = element_text(size = base_size),
      axis.text = element_text(size = base_size - 1),
      legend.title = element_text(size = base_size - 1),
      legend.text = element_text(size = base_size - 2),
      legend.position = "bottom",
      legend.key.size = unit(0.4, "cm"),
      plot.margin = margin(8, 8, 8, 8),
      strip.text = element_text(size = base_size, face = "plain")
    )
}

pal <- c("#2C3E50", "#E74C3C", "#3498DB", "#27AE60", "#8E44AD", "#F39C12")
theme_set(theme_tufte_paper())
