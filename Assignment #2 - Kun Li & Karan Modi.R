library(car)
# Load data
df = read.csv("HW2 regression dataset.csv",header=TRUE)

# As factor
df$trustad <- as.factor(df$trustad)

# Creat "season" to catch the pitchs happening at the late years
df$season <- ifelse(df$eq_volum >= 6221548.5, 1, 0)

# As factor
df$season <- as.factor(df$season)
attach(df)

# Modeling
mod = lm(log(eq_volum) ~ disacv_c + season + tvgrp_c + 
           trustad + fsi_holi + fsi_comp + itemstor )
summary(mod)

#VIF check
vif(mod)

plot(mod, which = 1) 

plot(mod, which = 3) 
