# Review Scope
AI product reviewer using NLP

## Introduction
This project is a product review analysis tool that uses NLP to analyze the sentiment of a product review.The backend is built using Django and the frontend is built using Vanilla html,css and Js. The NLP model is built using the NLTK library. The model is then used to predict the sentiment of the product review.

## Demo
![image](https://user-images.githubusercontent.com/84141920/234339448-b9dd8429-cd1e-4954-92b1-30162e63467c.png)

## Features
- User can enter a product link and the review text will be extracted from the product page on Amazon, Flipkart, etc.
- Based on the review text, the sentiment of the review is predicted.
- The sentiment is then displayed to the user along with a summarised version of the review and graphical representation of the sentiment.

## Components
- Chrome extension (entry point)
- Main Website page with user auth & history
- REST API to connect extension
- NLP model
- Database for user history and auth 
