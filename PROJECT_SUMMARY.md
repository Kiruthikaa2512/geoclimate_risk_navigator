## ** GeoClimate AI – Command Center**
**Author:** Kiruthikaa Natarajan Srinivasan  
**Date:** November 28, 2025  

A global supply chain risk intelligence platform for evaluating, simulating, and optimizing trade lanes.

**Overview**

Geoclimate AI was created as an inspiration from my work experience of being in the supply chain for a decade and the usecase that I have seen throughout. Supply chain global logistics is often fragile and breakable when there is a natural calamity or any other vulnerability. 

GeoClimate AI is an end-to-end risk intelligence platform designed to help organizations analyze international supply chains using four key domains: geopolitics, climate vulnerability, logistics reliability, and cybersecurity exposure. It integrates data modeling, mapping, simulation, and generative AI to form a decision-support system for global operations.

The platform acts as a lightweight digital twin of trade networks, enabling teams to understand lane risks, simulate disruptions, compare alternatives, and generate decision-ready reports.

## Inspiration
Coming from the decade of supply chain experience, and working as an EDI Project manager and currently pursuing my second Master's in Data Analytics, I have seen how fragile and unpredictable it can be when it comes to logistics and transportation. As we all know, during COVID, we had a major setback in terms of commuting and transporting things due to the pandemic restrictions. That gave me a spark to work on this niche space of exploring the possibilities with AI integrated into supply chain logistics. Companies still rely on static tools even as climate volatility, geopolitical tensions, port congestion, and cyber threats increase. I wanted to build a system that merges real-world supply chain intuition with AI-style intelligence to make routing decisions faster and smarter. This tool that I developed would help achieve the same. 

## What it does
GeoClimate AI is an end-to-end risk intelligence platform designed to help organizations analyze international supply chains using four key domains: geopolitics, climate vulnerability, logistics reliability, and cybersecurity exposure. It was designed to act as a digital twin of trade networks, enabling teams to understand lane risks, simulate disruptions, compare alternatives, and generate decision-ready reports. Basically, this application has 5 modules. The first module is Route Analyzer, which recommends the safest, fastest, or most resilient mode between any two countries. The second module is the Scenario lab module lets users test out and simulate possible disruptions between the countries. The third module is Global Heatmap, which helps users to see on the map the impacted countries and hotspots visually. The AI Strategy room makes this tool very special as it is designed specifically to answer only the questions related to this app. It provides real-time strategy advice for the users. The fourth module we have is the Network Optimizer, which generates optimized routing alternatives.
The last module is Export Center, which lets users export summaries for leadership.

## How we built it
The app was built using Python and Streamlit for a fast and interactive interface experience for the users. A rule-based mock LLM engine for advisory responses. Used Python libraries like Plotly for maps, charts, and heatmaps. Custom CSS command center for modern UI theme.

## Challenges we ran into
As I have integrated AI responses into the project, the usage of the API key made me struggle for a few days, literally. Tried OpenAI's project key, but that was not working well, and the AI was unable to produce results and ran into errors. As the OpenAI key's API keys were paid and had limited options for free, I chose to switch to the Groq API key, and for some reason, ran into a similar error, though it was set in Streamlit's secrets. Understood that exploring with the API key can be tried in future enhancements and decided to simulate “AI-like” responses without real LLM APIs. But then, avoiding irrelevant AI responses when context changes has become another challenging part. Still fixed all the possible errors and made sure that the mock AI produces appropriate results. 

I also ran into issues when changing the theme and overall background color. I was not satisfied with the half white background, hence I tried all the possible combinations and ended up with mild yellow with a subtle and decent look. 

Pushing the app to production had issues with the version compatibility. I had to upgrade the requirements.txt to the most premium version of everything to make it work in production. 

## Accomplishments that we're proud of
Devpost Aethra's hackathon allowed me to build and complete a fully functional app from scratch, though I have built a lot of projects during my college coursework, but this one is very special as it was something that I tried from scratch with no guidance from my professor but the knowledge and hands-on we gained via assignments and rigorous projects helped me to achieve this today. 

## What we learned
I learnt that blending domain experience with AI/Data Analytics helps make incredible projects and can really solve a lot of real-world scenarios in the industry. I am motivated to try a lot of new topics with the experience I gained while working on this project.

## What's next for GeoClimate AI – Command Center
This can be expanded to integrate real LLMs for more advanced strategic guidance.
We can add live data sources: weather, port congestion, sanctions, and disruptions.
I have also planned to build forecasting models for future lane risk. Additionally, we can expand this to achieve supplier-level details and SKU-level network views. This system can be evolved into a full digital twin of global logistics networks.
