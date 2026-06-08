# AIAP Technical Assessment — Decision Log

**Candidate name (as in NRIC):**

**Email (as used in your application):**

## Document was accidentally overwritten by AI. I am now rewriting it from scratch.
---

## A note on this document

This decision log is the primary instrument by which we understand your thinking. The questions below cover the reasoning behind your work — from how you define the problem at the start to the decisions you made during the work itself. Do answer all five questions in your own words. 

You may use AI assistance freely on the technical deliverables (the EDA and the ML pipeline), but this Decision Log itself should be written by you — it is the record of your own thinking that we cross-check against your chat history.


---

## 1. Clarifying questions

What questions would you ask to better define and narrow the problem statement? For each question, briefly explain how the answer would meaningfully change your approach. 

Note: If it helps your decision-making, you may assume and list out the stakeholders' likely answers.


What are the Key delivery Kpis for Drivers (referring to all delivery mediums)? How are they measured. Are there any incentives/ rewards for drivers who exceed performance targets? Conversely, are there any sanctions on Drivers who consistently fail to meet Kpis, Will these drivers be offered performance remediation opportunities and support to provide an opportunity for them to improve their performance (I.e if driver uses/ rent own car which frequently break down during the job, will company help to provide alternative options. i.e2 ,Also what are the redundancies for broken job equipment, such as reserve van   ). ## I'm trying to understand if the poor delivery performance are due drivers being overwhelmed or because of other causation such as an indifferent work environment.  


Similarly, What are the Key Kpis for fulfillment depots, are depot managers empowered to autonomously validate (i.e through A/B testing) potential solutions that might provide solutions? Are they adequately supported and authorised to implement validated solutions? Or will they be required to follow the SOP's word for word? ##Trying to determine the best choice of collecting and implementing data for the maximum benefit to organisation. Additionally, evauluate suitibility of implemeting further Machine Learning nodes (branches), long term might even be able to put up a plan for government grant and assistance.

What other solutions have been attempted as a remedy to the (trend of) decrease in customer satisfaction, before engaging us? How have you attempted to solve the delivery problems. ##Develop deeper understanding of the problem situation and why potential remedies failed- determine next course of action

Additionally, other than the decrease in customer satisfaction and delivery problems, what would you say are the other pain points? (i.e, Shopee forces MoveEasy to provide next day delivery at a very low bulk shipping cost per parcel, forcing MoveEasy to maximise and overload lots of parcel per driver to ensure profitability). ##Accessing other potential vectors to gather data for improvements.

Are there factors that are generally out of MoveEasy's control (such as customs clearance delays or late handoff by other furfilment partners). IS this information conveyed swiftly to customers to address potential customer fustration at the earliest opportunity (i.e on Move Easy's own tracking portal, shipping updates are quickly pushed 20.00 hrs Parcel Arrived at Changi Airport, awaiting customs clearance.) ## Maybe sometimes the disatisfaction is not objective and due to other human factors such as optics

If we cant hire more drivers, can we reduce the frequency of routes with the poor cost to performance ratio and route with poor, refocusing resources on improving customer satisfaction and profitability of high profitibility routes? Are we also able to implement alternative measures to reduce furfilment time and distance, such as opening a 5th depot in an under served district? ## Explore potential actionables on the table if, the convincing case can be presented with data.

Can you share with me some of the profitability and financial details of your company, such as the required gross profit per km per parcel? How are the various services (products) of your company performing, are they meeting the growth targets? ## Trying to Understand the actual needs of the company based on their objectives, rather than their own perception





---

## 2. Defining the Problem Statement

Restate, in your own words, the refined problem you decided to solve. List your key assumptions. Briefly note what other framings you considered, and what you deliberately left out or scoped down, and why.

Business is operating well over capacity. My analysis of feedbacks showed the most common complaints relates to late deliveries, while proportionally, the most common positive comments are about deliveries being on time (Meeting or exceeding the delivery window)

Moreover, the greatest cause of complaints and poor feedback are due to a combination of great delivery distances and too much backlog for drivers to deliver.

Other framing include, potentially single major clients were deviating (and demanding) enough that they were able to skew, however after examining the furfilment rates,  I realised that the VVIP shipping options which are usually the most time critical had the highest satisfaction rates and the fragility of item shipped through VVIP shipping had neglible difference.

Left out other scopes such as due to driver performance or poor average driver performance from certain branch or certain vehicle type are more likely to cause issues





---

## 3. Key decisions during Solution Development

Walk through three key decisions you made during Solution Development. For each: what options did you consider, what did you choose, and why? These can be technical (modelling choices, feature handling, evaluation metrics) or about the work itself (what to prioritise, what to drop, how to spend your time).


Cache, to improve performance of Machine learning pipeline, preventing needlessly reading of dataset everytime.

Manual cross checking of dataset to ensure data accuracy and prevent AI hallucination, but decision was largely depriciated due to shortness of time

Abandoning goal of ensure full context between sessions, too much perfomance overhead




---

## 4. Use of the AI assistant

Where did you use the AI assistant in this work? Give three specific examples of something the assistant suggested that you changed, rejected, or significantly modified — and explain your reasoning.


Claude overwrote my decision log, self explanatory, largely my fault due to infamilarity with default ai mkdown naming conventions. 

Chatgpt, suggesting me to copy 50 pages of chat transcript to provide context of previous session from different ai mode. AI started to lose contex

Chatgpt, suggesting that copilot (claude Haiku api), is unable to save context to perssitent memory and infer in subsequent sessions. False since, you wouldnt really be able to code with cli then, plus the app would be really inefficient and use up all internet


---

## 5. Next Steps

If you had one more week to continue this project, what would you do next, and why? What signals from your current work make those the right next steps?
USe know environment, I spent 3 days setting up, and repairing my environment
and use common prompts for reliability such as fail safe
1

**Your answer:**





---