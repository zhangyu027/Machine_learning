install.packages("dplyr")
require(dplyr)
require(tidyverse)

###create from long form to wide form##

setwd("//cnocfp01/rea$/Common/USER/yzhang/SGP whitepaper")
setwd("//CNOCMF06/Staff_Z$/yuzhang1/Desktop")

Gk1 <- read.csv("Gk1.csv")##
G12 <- read.csv("G12.csv")
G23 <- read.csv("G23.csv")

##Gk1##
Gk1_1 <- Gk1 %>% 
  select(c("StudentID","AcademicYearID.G1",	"GradeCode.G1",	"RITScore.G1"),)%>%
  pivot_wider(names_from = c(AcademicYearID.G1), values_from = c(GradeCode.G1,	RITScore.G1))
    
Gk1_k <- Gk1 %>% 
  select(c("StudentID","AcademicYearID.k",	"GradeCode.k",	"RITScore.k"),)%>%
  pivot_wider(names_from = c(AcademicYearID.k), values_from = c(GradeCode.k,	RITScore.k))
  
Gk1_wideform <- merge(Gk1_1, Gk1_k, by= "StudentID", all = TRUE)

Gk1_wideform_f <- Gk1_wideform%>%
  mutate(Grade_2016 = paste0(GradeCode.G1_2016, GradeCode.k_2016)) %>%
  mutate(Grade_2017 = paste0(GradeCode.G1_2017, GradeCode.k_2017)) %>%
  mutate(SS_2016 = paste0(RITScore.G1_2016, RITScore.k_2016))%>%
  mutate(SS_2017 = paste0(RITScore.G1_2017, RITScore.k_2017))

##G12##
G12_1 <- G12 %>% 
    select(c("StudentID","AcademicYearID.G1",	"GradeCode.G1",	"RITScore.G1"),)%>%
  pivot_wider(names_from = c(AcademicYearID.G1), values_from = c(GradeCode.G1, RITScore.G1))
  

G12_2 <- G12 %>% 
    select(c("StudentID","AcademicYearID.G2",	"GradeCode.G2",	"RITScore.G2"),)%>%
  pivot_wider(names_from = c(AcademicYearID.G2), values_from = c(GradeCode.G2,	RITScore.G2))


G12_wideform <- merge(G12_1, G12_2, by= "StudentID", all = TRUE)


G12_wideform_f <- G12_wideform%>%
  mutate(Grade_2016 = paste0(GradeCode.G2_2016, GradeCode.G1_2016)) %>%
  mutate(Grade_2017 = paste0(GradeCode.G2_2017, GradeCode.G1_2017)) %>%
  mutate(SS_2016 = paste0(RITScore.G2_2016, RITScore.G1_2016))%>%
  mutate(SS_2017 = paste0(RITScore.G2_2017, RITScore.G1_2017))
  

##G23##

G23_3 <- G23 %>% 
  select(c("StudentID","AcademicYearID.G3",	"GradeCode.G3",	"SBAScore"),)%>%
  pivot_wider(names_from = c(AcademicYearID.G3), values_from = c(GradeCode.G3,	SBAScore))

G23_2 <- G23 %>% 
  select(c("StudentID","AcademicYearID.G2",	"GradeCode.G2",	"RITScore"),)%>%
  pivot_wider(names_from = c(AcademicYearID.G2), values_from = c(GradeCode.G2,	RITScore))

G23_wideform <- merge(G23_3, G23_2, by= "StudentID", all = TRUE)

G23_wideform_f <- G23_wideform%>%
  mutate(Grade_2016 = paste0(GradeCode.G3_2016, GradeCode.G2_2016)) %>%
  mutate(Grade_2017 = paste0(GradeCode.G3_2017, GradeCode.G2_2017)) %>%
  mutate(SS_2016 = paste0(SBAScore_2016, RITScore_2016))%>%
  mutate(SS_2017 = paste0(SBAScore_2017, RITScore_2017))

write.csv(Gk1_wideform_f, file = "Gk1_wideform.csv")
write.csv(G12_wideform_f, file = "G12_wideform.csv")
write.csv(G23_wideform_f, file = "G23_wideform.csv")

  
  

