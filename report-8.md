# Project Proposal: Campus Events and Entertainment Center

## Project Overview

### Target Users

The primary users of the "Campus Events and Entertainment Center" are students, faculty, staff, and visitors of Southern University of Science and Technology (SUSTech). This system serves as a comprehensive platform for discovering, booking, and participating in a wide range of campus events.

### Functionalities

The system will offer the following key functionalities:

1. **Browsing Event Information**: Users can view details of various events categorized into academic, sports, cultural, etc. It includes a search feature and detailed event pages.
2. **Booking Tickets and Registration**: A secure system for booking and registration for events, integrated with multiple payment options.
3. **Event Reviews and User Communication**: A platform for user reviews, private messaging, and discussion forums.
4. **Event Recommendations**: Personalized event suggestions based on user preferences and history.
5. **Event Reminders and Notifications**: Timely reminders about upcoming events through different channels like app notifications, SMS, and emails.

### Expected Outcome

The goal is to enhance visibility and participation in campus events, providing an interactive and convenient platform for the SUSTech community to engage in campus cultural and academic activities.

## Preliminary Requirement Analysis

### Functional Requirements

1. **Event Information Browsing**:
    - Categorization of events.
    - Detailed information including organizer, description, venue (with maps), timing, and participation methods.
2. **Booking and Registration**:
    - Secure booking process.
    - Integration with various payment methods.
3. **User Reviews and Communication**:
    - Platform for posting reviews.
    - Messaging and forum features.
4. **Personalized Event Recommendations**:
    - Algorithm-based suggestions.
5. **Reminders and Notifications**:
    - Multi-channel event reminders.

### Non-Functional Requirements

1. **Usability**: Intuitive and user-friendly interface.
2. **Safety and Security**: Strong data encryption and privacy protection.
3. **Performance**: Efficient handling of high user traffic.
4. **Transparency**: Bias-free recommendation algorithms.

### Data Requirements

- A comprehensive database of campus events.
- Map data for event locations.
- User data for personalized services.

### Technical Requirements

- **Operating Environment**: Web and mobile platforms.
- **Tech Stack**: Front-end (React/Vue3), Back-end (Rust/Node.js/Python), Database (MongoDB/MySQL/PostgreSQL).
- **Integration**: Payment gateways, map services, notification systems, Recommender systems.

---

## Task Decomposition & Planning

### User Stories (Product Backlog)

1. As a SUSTech student, I want it can show various information such as categories, data and venues so that I can know if I will be interested and able to participate.
2. As a SUSTech student, I want the application to analyze my past activity participation and preferences, So that I can receive personalized activity recommendations on the homepage of the app
3. As a SUSTech student, I want to receive timely and accurate reminders for activities that I might be interested in, so that I can manage my schedule effectively and participate in events that align with my preferences
4. As a sustech student, I want to share and view contents on the platform, so that I can get or share news on campus and feel connected to the community
5. As a SUSTech student, I want I can easily reserve tickets for the campus music concert, receive instant confirmation and an electronic ticket after payment, ensuring a seamless booking process and prioritizing data security and user privacy.
### TODO

- The event details page displays information about the organizer, a description of the event, the location (with map markings), the time, and how to participate
- Provides a search function that allows users to search for events based on keywords
- Map data is available to show the location of the event
- Integrated payment function, support multiple payment methods
- Provide instant booking confirmation and e-ticketing
- Enables data encryption of payments and user privacy protection
- Implement private messaging between users
- Implement a posts feature that allows users to initiate topic discussions
- Enabling content review and community rule enforcement
- Recommended activities based on user historical activity engagement and preference algorithms
- Optimize recommendation systems using machine learning and data mining techniques
- Ensure transparency and unbiased recommendation algorithms
- Send users reminders of upcoming events via in-page notifications
- Email alerts to subscribers that an event is about to start
- Ensure timeliness and accuracy of reminders

### Roadmap

- Start Date: 2024.3.18
- Duration: 9 weeks (end by Week 9)

---

## AI Usage

### Usage of AI in Proposing Features

**Yes, ChatGPT4 was used.**

- **Prompt Used**: "软工proposal 目标用户：南科大师生功能：1.可以浏览南科大活动的具体信息，时间地点 2.可以预订活动门票，报名活动 3.可以对活动评论，可以发帖，用户间可以交流 4.有活动推荐 5.事件提醒和通知预期目标：可以让南科大师生了解到南科大的活动并可以报名，也可以分享自己对活动的看法 需求： 1.功能性需求： 2.非功能性需求： 3.数据需求： 4.技术需求：补全功能的具体细节和需求."
- **Usage**: This prompt was used to auto-generate a list of features and requirements for the project, blending inputs from the project list and AI insights.

### AI for Preliminary Requirement Analysis

**Yes, ChatGPT4 was used.**

- **Prompt Used**: Similar to the feature proposal prompt, focusing on detailing the functional, non-functional, data, and technical requirements.
- **Usage**: The AI response served as a structured breakdown of the necessary requirements for the project, offering a preliminary foundation for further development.

### AI in Generating User Stories

**Yes, ChatGPT4 was used.**

- **Prompt Provided to AI**: We used the template from the course to list each requirement and asked AI to create user stories accordingly.
- **Usage**: The AI-generated user stories directly informed the project planning, ensuring that user needs and goals were clearly defined and addressed.

### AI in Generating Tasks (TODOs)

**Yes, ChatGPT4 was used.**

- **Prompt Used**: AI was tasked with translating the user stories into actionable tasks suitable for inclusion in a sprint backlog.
- **Usage**: The AI-generated list of tasks was adopted as an initial backlog, setting the stage for the project's first sprint and guiding the delegation of tasks within the team.

### Observations on AI Usage

- The AI-generated content provided a valuable starting point and framework for the project.
- However, it was necessary to adapt and refine the AI-generated material to ensure it accurately met the project's specific needs and context.
- AI was particularly useful in expediting the brainstorming and initial drafting phases, while human oversight was crucial in aligning these ideas with practical implementation and project goals.

### AI Implementation Details

- AI tools such as ChatGPT were employed to generate ideas and refine project requirements.
- The AI-generated responses were used as a basis and further customized to fit the project's specific needs.