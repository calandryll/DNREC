library(shiny)
library(ggplot2)
library(dplyr)
library(tidyr)
#library(plotly)

ui = fluidPage(
  theme = 'bootsrap.css',
  titlePanel('DNREC MST Pilot Study'),
  selectInput('var',
                    label = 'Choose Month to display',
                    choices = list('March', 'April', 'May', 'June', 'June Rain'),
                    selected = 'March'
    ),
  mainPanel(
    
    # this is an extra div used ONLY to create positioned ancestor for tooltip
    # we don't change its position
    div(
      plotOutput("plot1", hover = hoverOpts("plot_hover", delay = 100, delayType = "debounce")),
      uiOutput("hover_info")
    )
  )
)


server = function(input, output) {
  st = read.csv('sourcetracker.csv')
  st2 = st %>% gather(Factor, SampleID, 2:11)
  colnames(st2) = c('SampleID', 'STORET', 'Site', 'Month', 'Path', 'Factor', 'Percent') 
  output$plot1 = renderPlot({
    st.plot = st2 %>% filter(Month == input$var) %>% ggplot() +
      geom_bar(aes(y = Percent, x = Path, fill = Factor), stat = 'identity', position = position_fill(reverse = TRUE)) +
      scale_fill_manual(name="Fecal\nSource", values = c('#a50026','#d73027','#f46d43','#fdae61','#fee090','#e0f3f8','#abd9e9','#74add1','#4575b4','#313695'), guide = guide_legend())  +
      theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), legend.position = 'bottom', axis.title.x = element_blank(), axis.text = element_text(size = 20), axis.title.y = element_text(size = 20, face = 'bold'), legend.text = element_text(size = 20), legend.title = element_text(size = 20)) +
      labs(y = 'Percentage') + 
      scale_x_continuous(breaks = c(1,2,3,4,5,6,7), labels = c('Jimtown\nRd', 'Bundicks\nBranch', 'Goslee\nPond', 'Misty\nLane', 'Rt.\n24', 'West\nLane', 'Mouth of\nLove Creek')) + 
      scale_y_continuous(labels = scales::percent)
    
      print(st.plot)
    })
  output$hover_info = renderUI({
    hover = input$plot_hover
    point = nearPoints(st2, hover, threshold = 5, maxpoints = 1, addDist = TRUE)
    if (nrow(point) == 0) return(NULL)
    
    # calculate point position INSIDE the image as percent of total dimensions
    # from left (horizontal) and from top (vertical)
    left_pct = (hover$x - hover$domain$left) / (hover$domain$right - hover$domain$left)
    top_pct = (hover$domain$top - hover$y) / (hover$domain$top - hover$domain$bottom)
    
    # calculate distance from left and bottom side of the picture in pixels
    left_px = hover$range$left + left_pct * (hover$range$right - hover$range$left)
    top_px = hover$range$top + top_pct * (hover$range$bottom - hover$range$top)
    
    # create style property fot tooltip
    # background color is set so tooltip is a bit transparent
    # z-index is set so we are sure are tooltip will be on top
    style = paste0("position:absolute; z-index:100; background-color: rgba(245, 245, 245, 0.85); ",
                    "left:", left_px + 2, "px; top:", top_px + 2, "px;")
    
    # actual tooltip created as wellPanel
    wellPanel(
      style = style,
      p(HTML(paste0("<b>", point$Factor, '</b> ', point$Percent)))
    )
  })

}

shinyApp(ui, server)