# Sarvam project Overview

## Introduction

Welcome to the project repository! This project is divided into two main parts:

- **Part-1**: This directory contains Question and answering on PDF using RAG pipeline
- **Part-2**: This directory contains Agents on PDF, URL, Google search tool which can invoke based on question.

## Problem statement:
- Assignment Part 1: Building a RAG system
RAG systems are one of the most widely used patterns which is powering a lot of AI applications. The basic idea is using an external data source in a vector database along with an LLM. You have to build a RAG system which works on a medium sized dataset. In this case you would be working with NCERT PDF text.
Build a RAG system and serve it using a FastAPI endpoint. You should be able to send a query and get a response back.
You can use any frontend you see fit to showcase this endpoint.

- Assignment Part 2: Building an Agent that can perform smart actions based on the user’s query. Extend the service and host another endpoint for the agent.
The agent should be reliably able to decide when to call the VectorDB and when to not. Ex: Hello -> should not call the VectorDB.
Secondly, introduce at least ONE more action / tool in your system that the Agent can invoke based on the user’s query. Bonus points for more creative actions!

- Assignment Part 3: Give a Voice to your Agent. This is OPTIONAL that you can attempt for bonus points!
Use Sarvam’s APIs to add voice to your Agent.


## Execution Structure

- **`part-1/`**: Detailes workflow is present in **Readmd.me** file to execute the part-1 problem statement
- **`part-2/`**: Detailes workflow is present in **Readmd.me** file to execute the part-12 problem statement

## Note:
- **part-3**: The voice is added to the bot in agent.

## Assignments executed:
- **Assignment part-1**: Executed present in part-1
- **Assignment part-2**: Executed present in part-2
- **Assignment part-3**: Executed present in part-2. Added voice to part-2 agent.

