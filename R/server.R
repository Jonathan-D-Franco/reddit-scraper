#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

# importing libraries for reading csv and creating plots
library(shiny)
library(readr)
library(ggplot2)

# read data
reddit_data <- read_csv("data/data.csv")

# Define server logic required to draw a scatterplot
shinyServer(function(input, output, show_col_types = FALSE) {

    output$Plot <- renderPlot({

        # draw the scatterplot
        p <- ggplot(reddit_data, aes(x = comments, y = upvotes), xlab='comments', ylab='upvotes') + geom_point() +
          ylim(0,input$yAxis)+ xlim(0,input$xAxis) + ggtitle("upvotes vs comments")
        # checks if the radio button is allowing order to show or not
        if(input$Order == "On") p + geom_point(aes(color=...1)) + labs(color="Order")
        else p

    })
    # renders the text of mouse hovering to give a better sense of the graph
    output$info <- renderText({
      # function to eat up any time im not hovering and then send the text when I am
      xy_str <- function(e) {
        if(is.null(e)) return("NULL\n")
        paste0("comments=", round(e$x, 1), " upvotes=", round(e$y, 1), "\n")
      }
      paste0("hover: ", xy_str(input$plot_hover))
    })
    # rendering the link of the data point that i just clicked on
    output$tab <- renderUI({
      # also makes sure that null doesnt appear and if you click on nothing that doesnt appear either
      link_str <- function(e) {
        if(is.null(e)) return("\n")
        link = nearPoints(reddit_data,input$plot_click, maxpoints = 1)[6]
        if(nrow(link) == 0) return("\n")
        url <- a("link", href=link)
        return(url) 
        }
      tagList("reddit:",href=link_str(input$plot_click))
    })
})
