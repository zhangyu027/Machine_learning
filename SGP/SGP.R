install.packages("SGP")
install.packages("psych")
install.packages("dplyr")
require(SGP)
require(dplyr)
require(tidyverse)
install.packages("Y:/USER/wlesbenshade/SPSTools-builds/spsTools_0.2.0.tar.gz")


#### G12 MAP quantile growth percentile###

setwd("//cnocfp01/rea$/Common/USER/yzhang")
setwd("//CNOCMF06/Staff_Z$/yuzhang1/Desktop")
setwd("C:/Users/zhang/OneDrive/Desktop")

sgp <- read.csv("SeattleSGP_Reading_2011_G8-G10.csv")
sgpk1 <- read.csv("sgpk1_wideform_2018.csv")##
sgpk1 <- read.csv("sgpk1_wideform_2017.csv")##
sgpk1 <- read.csv("sgpk1_wideform_2016.csv")##

sgpG2 <- read.csv("sgpG2_wideform_2018.csv")##
sgpG2 <- read.csv("sgpG2_wideform_2017.csv")##
sgpG2 <- read.csv("sgpG2_wideform_2016.csv")##
sgpG3<- read.csv("sgpG3_wideform_2018.csv")##
sgpG3<- read.csv("sgpG3_wideform_2017.csv")##
sgpG3<- read.csv("sgpG3_wideform_2016.csv")##


##test##

sgp_g8_v2 <- studentGrowthPercentiles(
  panel.data=sgp,
  sgp.labels=list(my.year=2010, my.subject="Reading"),
  percentile.cuts=c(1,35,65,99),
  grade.progression=c(8,9))

sgp_g8_v3 <- studentGrowthPercentiles(
  panel.data=sgp,
  sgp.labels=list(my.year=2011, my.subject="Reading"),
  percentile.cuts=c(1,35,65,99),
  grade.progression=c(8,9))

sgp_g8<- rbind(
  sgp_g8_v2$SGPercentiles$READING.2010,
  sgp_g8_v2$SGPercentiles$READING.2011)

sgp_g8<- sgp%>%
  distinct(ID,.keep_all = TRUE)

write.csv(sgp_g8, file="sgpreading_2011_gall.csv", row.names=FALSE, quote=FALSE, na="")


##Grade1##

sgp_g1_v1 <- studentGrowthPercentiles(
  panel.data=sgpk1,
  sgp.labels=list(my.year=2016, my.subject="Reading"),
  percentile.cuts=c(1,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,99),
  grade.progression=c(0,1))


sgp_g1_v2 <- studentGrowthPercentiles(
  panel.data=sgpk1,
  sgp.labels=list(my.year=2017, my.subject="Reading"),
  percentile.cuts=c(1,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,99),
  grade.progression=c(0,1))

sgp_g1_v3 <- studentGrowthPercentiles(
  panel.data=sgpk1,
  sgp.labels=list(my.year=2018, my.subject="Reading"),
  percentile.cuts=c(1,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,99),
  grade.progression=c(0,1))


##Grade2##
sgp_g2_v1 <- studentGrowthPercentiles(
  panel.data=sgpG2,
  sgp.labels=list(my.year=2016, my.subject="Reading"),
  percentile.cuts=c(1,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,99),
  grade.progression=c(1,2))


sgp_g2_v2 <- studentGrowthPercentiles(
  panel.data=sgpG2,
  sgp.labels=list(my.year=2017, my.subject="Reading"),
  percentile.cuts=c(1,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,99),
  grade.progression=c(1,2))

sgp_g2_v3 <- studentGrowthPercentiles(
  panel.data=sgpG2,
  sgp.labels=list(my.year=2018, my.subject="Reading"),
  percentile.cuts=c(1,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,99),
  grade.progression=c(1,2))


##Grade3##

sgp_g3_v1 <- studentGrowthPercentiles(
  panel.data=sgpG3,
  sgp.labels=list(my.year=2016, my.subject="ELA"),
  percentile.cuts=c(1,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,99),
  grade.progression=c(2,3))


sgp_g3_v2 <- studentGrowthPercentiles(
  panel.data=sgpG3,
  sgp.labels=list(my.year=2017, my.subject="ELA"),
  percentile.cuts=c(1,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,99),
  grade.progression=c(2,3))

sgp_g3_v3 <- studentGrowthPercentiles(
  panel.data=sgpG3,
  sgp.labels=list(my.year=2018, my.subject="ELA"),
  percentile.cuts=c(1,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,99),
  grade.progression=c(2,3))


identical(sgp_g3_v1$SGPercentiles, sgp_g3_v2$SGPercentiles)


##combine files##

sgp_g2<- rbind(
  sgp_g2_v1$SGPercentiles$READING.2016,
  sgp_g2_v2$SGPercentiles$READING.2017,
  sgp_g2_v2$SGPercentiles$READING.2018)

sgp_g3 <- rbind(
  sgp_g3_v1$SGPercentiles$ELA.2016,
  sgp_g3_v2$SGPercentiles$ELA.2017,
  sgp_g2_v2$SGPercentiles$READING.2018)


write.csv(sgp_g3, file="sgpG3.csv", row.names=FALSE, quote=FALSE, na="")

sgp12_d<- sgp12%>%
  distinct(ID,.keep_all = TRUE)

