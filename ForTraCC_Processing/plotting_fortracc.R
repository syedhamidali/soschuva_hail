#-------------------------------------------------------------------------------
#-- Exporting entries from "processing_fortracc.R"
#-- Plotting clusters superimposed on radar
#-- Plotting selected systems' trackings, dBZ and size during life cycle
#-------------------------------------------------------------------------------

# Loading necessary scripts and packages
require(scales)
require(cptcity)
# Other necessary packages are called in this script
source("ForTraCC_Processing/processing_fortracc.R")

# Language of the plots
lang <- "en"  # "pt-br"

# REMOVING SECOND 2017-03-14 FAMILY
selected_fams <- selected_fams[-4]
selected_fams_df$lon_hailpad[selected_fams_df$case == "Case 2017-03-14 "][1] <- data_hailpads[4,3]
selected_fams_df$lat_hailpad[selected_fams_df$case == "Case 2017-03-14 "][1] <- data_hailpads[4,2]
selected_fams_df$date_hailpad[selected_fams_df$case == "Case 2017-03-14 "][1] <- "2017-01-01 18:00:00"
selected_fams_df <- selected_fams_df %>%
  filter(case != "Case 2017-03-14  ")

# Selecting part of the families -----------------------------------------------
selected_fams <- selected_fams[c(3,4)]
selected_fams_df <- selected_fams_df %>%
  filter(case == "Case 2017-03-14 " | case == "Case 2017-03-14  " | case == "Case 2017-11-15 ")
data_hailpads <- data_hailpads[3:5,]

# Plotting cappi + clusters in specific times (defined by "n")
# n <- 64
#
# row.names(data_cappis[[n]]) <- sort(lon_vector); colnames(data_cappis[[n]]) <- lat_vector
# cappi <- melt(data_cappis[[n]]) %>% na.omit()
# row.names(data_clusters[[n]]) <- sort(lon_vector); colnames(data_clusters[[n]]) <- lat_vector
# cluster <- melt(data_clusters[[n]]) %>% na.omit()
# labels_cluster <- cluster %>% group_by(value) %>%
#   summarise(Var2 = mean(Var2), Var1 = mean(Var1)) %>% ungroup()
#
# ggplot() +
#   scale_x_continuous(limits = lims_in_plot$lon) + scale_y_continuous(limits = lims_in_plot$lat) +
#   geom_raster(data = cappi, aes(x = Var1, y = Var2, fill = value)) +
#   geom_tile(data = cluster, aes(x = Var1, y = Var2), fill = "black", alpha = 0.5) +
#   geom_point(data = data_hailpads, aes(x = lon, y = lat), pch = 20, size = 5) +
#   geom_path(data = fortify(cities), aes(long, lat, group = group), inherit.aes = F, colour = "gray50") +
#   geom_label(data = labels_cluster, aes(x = Var1, y = Var2, label = value), nudge_y = 0.05, size = 2.5) +
#   scale_fill_distiller(palette = "Spectral", limits = c(10,70)) +
#   labs(title = paste(dates_clusters_cappis[n], "CAPPI 3 km"), x = "Longitude", y = "Latitude",
#        fill = "Z (dBZ)")
#
# Plotting only clusters to highlight a specific cluster
# image.plot(data_clusters[[n]], x = lon_matrix, y = lat_matrix, zlim = c(83,85))


# Plotting trajectories for all cases
theme_set(theme_bw())

if(lang == "pt-br"){
    shape_labs <-  c("Continuidade", "Fusão", "Novo", "Separação")
    shape <- "Classificação"
    color <- "Hora (UTC)"
    ggname <- "ForTraCC_Processing/figures/trajectories_cases_ptbr.png"
} else{
    shape_labs <- c("Continuity", "Merge", "New", "Split")
    shape <- "Classification"
    color <- "Time (UTC)"
    ggname <- "ForTraCC_Processing/figures/trajectories_cases.png"
}

ggplot(data = selected_fams_df) +
  scale_x_continuous(limits = lims_in_plot$lon) + 
  scale_y_continuous(limits = lims_in_plot$lat) +
  # geom_point(aes(x = lon, y = lat, size = size, color = hour), alpha = 0.1) +
  geom_point(aes(x = lon_hailpad, y = lat_hailpad), pch = 17, size = 2) +
  geom_path(aes(x = lon, y = lat, color = hour), size = 0.5) +
  geom_point(aes(x = lon, y = lat, color = hour, shape = class), 
             size = 2.5, position = "jitter") +
  geom_path(data = fortify(cities), aes(long, lat, group = group), inherit.aes = F, 
            colour = "gray50", size = 0.2) +
  # scale_size_continuous(range = c(0, 20)) +
  scale_color_gradientn(colours = cpt(pal = "oc_zeu"), labels = date_format("%H%M"),
                        breaks = pretty_breaks(n = 10), trans = time_trans()) +
  scale_shape_manual(values = c(20, 15, 18, 0), labels = shape_labs) +
  labs(x = expression("Longitude (" * degree * ")"), y = expression("Latitude (" * degree * ")"),
    color = color, shape = shape) +  # pt-br
  guides(size = "none", color = guide_colorbar(barheight = 12)) +
  theme(
    plot.background = element_rect(fill = "transparent", color = "transparent"),
    legend.background = element_rect(fill = "transparent")
  ) +
  # theme(legend.position = "bottom") + #-- For less plots
  # guides(size = "none", color = guide_colorbar(barwidth = 15), 
  #   shape = guide_legend(nrow = 2, byrow = T)) + #-- For less plots
  facet_wrap(~case)
ggsave(ggname, width = 8.5, height = 4.3, bg = "transparent")
# ggsave("ForTraCC_Processing/figures/trajectories_cases_less.png", 
#   width = 7.5, height = 3.25,  bg = "transparent") #-- For less plots

# Generating plots of life cycle of dBZ max and area for future plot
plt_dbz <- ggplot(data = selected_fams_df) +
  scale_x_datetime(labels = date_format("%H%M")) +
  geom_path(aes(x = hour, y = pmax), color = "tomato") +
  geom_vline(aes(xintercept = date_hailpad), linetype = "dashed") +
  theme(
    plot.background = element_rect(fill = "transparent", color = "transparent"),
    legend.background = element_rect(fill = "transparent")
  ) +
  labs(x = "Time (UTC)", y = "Max 3km Reflectivity (dBZ)") +
  # labs(x = "Hora (UTC)", y = "Refletividade Máx em 3km (dBZ)") +  # pt-br
  facet_wrap(case ~ ., scales = "free_x", ncol = 1) +
  theme(strip.text = element_blank())

plt_size <- ggplot(data = selected_fams_df) +
  scale_x_datetime(labels = date_format("%H%M")) +
  geom_path(aes(x = hour, y = size), color = "navyblue") +
  theme(
    plot.background = element_rect(fill = "transparent", color = "transparent"),
    legend.background = element_rect(fill = "transparent")
  ) +
  geom_vline(aes(xintercept = date_hailpad), linetype = "dashed") +
  labs(x = "Time (UTC)", y = expression("Area ("*km^2*")")) +
  # labs(x = "Hora (UTC)", y = expression("Tamanho ("*km^2*")")) +  # pt-br
  facet_wrap(case ~ ., scales = "free", ncol = 1) +
  theme(strip.text = element_blank())

# Saving variables -------------------------------------------------------------
save.image("ForTraCC_Processing/fortracc_data.RData")
