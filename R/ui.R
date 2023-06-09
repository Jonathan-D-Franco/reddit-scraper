#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

# imported themes just to make it look nicer
library(shiny)
library(shinythemes)

# Define UI for application that makes an interactable scatterplot
shinyUI
  list(fluidPage(
    # Theme 
    theme = shinytheme("cyborg"),
      # Application title
      titlePanel("League of Legends Subreddit"),
          # side panel for slide bars
          sidebarPanel(
            # these are to better examine the graph and data since there are a lot of outliers
            sliderInput("xAxis", "scale of X", 1, 2000, 2000),
            sliderInput("yAxis", "scale of Y", 1, 5000, 4000),
            # enhance the look of the graph by representing the order in which the website displays these posts
            radioButtons("Order", "Do you want to see the order?", choices = c("On","Off"))
          ),
  
          # Show a plot 
          mainPanel(
              # includes hovering and clicking for our benefit
              plotOutput("Plot", click = "plot_click", hover = 'plot_hover'),
              # used for the hovering
              verbatimTextOutput('info'),
              # used to display link
              uiOutput('tab')
          ))
)
