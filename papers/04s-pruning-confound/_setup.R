library(arrow)
library(dplyr)
library(ggplot2)
library(patchwork)

theme_set(theme_minimal(base_size = 11))

data_dir <- file.path(dirname(dirname(getwd())), "data")

read_experiment <- function(experiment_name) {
  path <- file.path(data_dir, experiment_name, "session_metrics.parquet")
  if (file.exists(path)) {
    read_parquet(path)
  } else {
    warning(paste("No data found for", experiment_name))
    NULL
  }
}

read_weights <- function(experiment_name) {
  path <- file.path(data_dir, experiment_name, "weight_snapshots.parquet")
  if (file.exists(path)) {
    read_parquet(path)
  } else {
    warning(paste("No weight data found for", experiment_name))
    NULL
  }
}
