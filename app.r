library(shiny)
library(ggplot2)
library(dplyr)
library(tidyr)
library(plotly)

ui = fluidPage(
  theme = 'bootsrap.css',
  titlePanel('DNREC MST Pilot Study'),
  selectInput('var',
                    label = 'Choose Month to display',
                    choices = list('March', 'April', 'May', 'June', 'June Rain'),
                    selected = 'March'
      ),
  plotOutput('plot1', width = '100%', height = '750px')
  )

server = function(input, output) {
  st = read.csv('sourcetracker.csv')
  st2 = st %>% gather(Factor, SampleID, 2:11)
  colnames(st2) = c('SampleID', 'STORET', 'Site', 'Month', 'Path', 'Factor', 'Percent') 
  output$plot1 = renderPlot({
    st.plot = st2 %>% filter(Month == input$var) %>% ggplot() +
      geom_bar(aes(y = Percent, x = Path, fill = Factor), stat = 'identity', position = position_fill(reverse = TRUE)) +
      scale_fill_manual(name="Fecal\nSource", values = c('#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#e0e0e0','#bababa','#878787','#4d4d4d','#1a1a1a'), guide = guide_legend())  +
      theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), legend.position = 'bottom', axis.title.x = element_blank(), axis.text = element_text(size = 20), axis.title.y = element_text(size = 20, face = 'bold'), legend.text = element_text(size = 20), legend.title = element_text(size = 20)) +
      labs(y = 'Percentage') + 
      scale_x_continuous(breaks = c(1,2,3,4,5,6,7), labels = c('Jimtown\nRd', 'Bundicks\nBranch', 'Goslee\nPond', 'Misty\nLane', 'Rt.\n24', 'West\nLane', 'Mouth of\nLove Creek')) + 
      scale_y_continuous(labels = scales::percent)
    
    print(st.plot)
  })
}

shinyApp(ui, server)