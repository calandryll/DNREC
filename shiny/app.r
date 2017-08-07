library(shiny)
library(ggplot2)
library(dplyr)
library(tidyr)
library(ggiraph)
#library(plotly)

ui = fluidPage(
  theme = 'bootsrap.css',
  titlePanel('DNREC MST Pilot Study'),
  selectInput('var',
              label = 'Choose Month to display',
              choices = list('March', 'April', 'May', 'June', 'June Rain'),
              selected = 'March'
  ),
  ggiraphOutput('plot', height = 800)
)

server = function(input, output) {
  theme_set(theme_bw())
  tooltip_css = "background-color:black;color:white;font-style:bold;padding:10px;border-radius:10px 10px 10px 10px;"
  st = read.csv('sourcetracker.csv')
  st2 = st %>% gather(Factor, SampleID, 2:11)
  colnames(st2) = c('SampleID', 'STORET', 'Site', 'Month', 'Path', 'Factor', 'Percent')
  st2 = st2 %>% mutate(Tooltip = paste(Factor, Percent, sep = ': '))
  output$plot = renderggiraph({
    st.plot = st2 %>% filter(Month == input$var) %>% ggplot() +
      geom_bar_interactive(aes(y = Percent, x = Path, fill = Factor, tooltip = Tooltip), stat = 'identity', position = position_fill(reverse = TRUE)) +
      scale_fill_manual(name="Fecal\nSource", values = c('#a50026','#d73027','#f46d43','#fdae61','#fee090','#e0f3f8','#abd9e9','#74add1','#4575b4','#313695'), guide = guide_legend())  +
      theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), legend.position = 'bottom', axis.title.x = element_blank(), axis.title.y = element_text(face = 'bold'), legend.title = element_text(face = 'bold')) +
      labs(y = 'Percentage') + 
      scale_x_continuous(breaks = c(1,2,3,4,5,6,7), labels = c('Jimtown\nRd', 'Bundicks\nBranch', 'Goslee\nPond', 'Misty\nLane', 'Rt.\n24', 'West\nLane', 'Mouth of\nLove Creek')) + 
      scale_y_continuous(labels = scales::percent)
    ggiraph(code = print(st.plot), selection_type = 'single', zoom_max = 5, tooltip_extra_css = tooltip_css, tooltip_opacity = 0.75)
  })
}

shinyApp(ui, server)