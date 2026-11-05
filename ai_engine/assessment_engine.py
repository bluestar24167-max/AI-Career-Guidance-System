"""Job-specific assessment and post-assessment analysis services."""

import json
import random
import requests

from ai_engine.roadmap import build_learning_roadmap


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"


# ============================================================
# ROLE COMPETENCY MAP
# ============================================================

ROLE_COMPETENCIES = {
    "ai engineer": [
        "Python programming",
        "data preprocessing",
        "feature engineering",
        "machine learning algorithms",
        "model training",
        "model evaluation",
        "overfitting and generalization",
        "deep learning",
        "model deployment",
        "AI debugging",
    ],

    "machine learning engineer": [
        "Python programming",
        "data preprocessing",
        "feature engineering",
        "machine learning algorithms",
        "model training",
        "model evaluation",
        "overfitting and generalization",
        "deep learning",
        "model deployment",
        "ML debugging",
    ],

    "data scientist": [
        "Python",
        "SQL",
        "statistics",
        "probability",
        "data cleaning",
        "exploratory data analysis",
        "feature engineering",
        "machine learning",
        "model evaluation",
        "data communication",
    ],

    "data analyst": [
        "SQL",
        "data cleaning",
        "exploratory data analysis",
        "statistics",
        "data visualization",
        "business metrics",
        "data interpretation",
        "reporting",
        "dashboards",
        "data storytelling",
    ],

    "backend developer": [
        "backend programming",
        "HTTP and REST APIs",
        "Django or backend frameworks",
        "SQL and databases",
        "database optimization",
        "authentication",
        "authorization",
        "API design",
        "error handling",
        "backend testing",
    ],

    "software engineer": [
        "programming",
        "data structures",
        "algorithms",
        "object-oriented programming",
        "API development",
        "databases",
        "software architecture",
        "testing",
        "debugging",
        "version control",
    ],

    "software developer": [
        "programming",
        "data structures",
        "algorithms",
        "object-oriented programming",
        "API development",
        "databases",
        "software architecture",
        "testing",
        "debugging",
        "version control",
    ],

    "full stack developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "frontend development",
        "REST APIs",
        "backend programming",
        "SQL and databases",
        "authentication",
        "debugging",
        "deployment",
    ],

    "web developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "responsive design",
        "browser fundamentals",
        "REST APIs",
        "frontend debugging",
        "accessibility",
        "performance",
        "deployment",
    ],
}


# ============================================================
# FALLBACK QUESTIONS
# ============================================================

def _fallback_questions_for_role(role):
    """
    Create a safe fallback question set for one specific role.

    These questions are intentionally more practical than the
    original fallback questions so that invalid Ollama output
    does not result in an extremely easy assessment.
    """

    role_lower = role.lower()

    # --------------------------------------------------------
    # AI ENGINEER / MACHINE LEARNING
    # --------------------------------------------------------

    if "ai engineer" in role_lower or "machine learning" in role_lower:

        questions = [
            {
                "question": (
                    "A training dataset contains numeric features with very "
                    "different scales. Which step is most appropriate before "
                    "using a distance-based model?"
                ),
                "options": [
                    "Scale the numeric features using a suitable method",
                    "Remove every feature with a large numeric value",
                    "Duplicate the rows until all values look similar",
                    "Convert every numeric feature directly into text",
                ],
                "answer": "Scale the numeric features using a suitable method",
                "skill": "Data preprocessing",
                "difficulty": "Foundation",
                "question_type": "Applied",
                "concept": "Feature scaling",
            },
            {
                "question": (
                    "An ML model performs very well on training data but much "
                    "worse on unseen validation data. What is the most likely issue?"
                ),
                "options": [
                    "The model is overfitting the training data",
                    "The model has completely avoided the training data",
                    "The dataset automatically became perfectly balanced",
                    "The validation set is always expected to score higher",
                ],
                "answer": "The model is overfitting the training data",
                "skill": "Model evaluation",
                "difficulty": "Foundation",
                "question_type": "Scenario",
                "concept": "Overfitting",
            },
            {
                "question": (
                    "You discover that a feature contains missing values before "
                    "training a model. What should you do first?"
                ),
                "options": [
                    "Investigate the missingness and choose suitable treatment",
                    "Replace every missing value with zero immediately",
                    "Delete the entire feature without checking its importance",
                    "Train the model and ignore the missing values completely",
                ],
                "answer": "Investigate the missingness and choose suitable treatment",
                "skill": "Data preprocessing",
                "difficulty": "Intermediate",
                "question_type": "Decision Making",
                "concept": "Missing data",
            },
            {
                "question": (
                    "A binary classifier has 98% accuracy, but only 2% of the "
                    "samples belong to the positive class. Why might accuracy "
                    "be misleading?"
                ),
                "options": [
                    "A model predicting mostly the majority class can score highly",
                    "Accuracy always becomes zero when classes are imbalanced",
                    "Binary classification cannot be evaluated using accuracy",
                    "The positive class is automatically treated as incorrect",
                ],
                "answer": "A model predicting mostly the majority class can score highly",
                "skill": "Model evaluation",
                "difficulty": "Intermediate",
                "question_type": "Scenario",
                "concept": "Class imbalance",
            },
            {
                "question": (
                    "A feature contains information that would only be known "
                    "after the prediction time in production. What problem does this create?"
                ),
                "options": [
                    "It can introduce data leakage and unrealistic model performance",
                    "It automatically improves production generalization",
                    "It guarantees the model will require fewer training examples",
                    "It converts the prediction problem into unsupervised learning",
                ],
                "answer": "It can introduce data leakage and unrealistic model performance",
                "skill": "Feature engineering",
                "difficulty": "Intermediate",
                "question_type": "Decision Making",
                "concept": "Data leakage",
            },
            {
                "question": (
                    "A model performs well during training but its validation "
                    "score changes greatly between different data splits. What "
                    "should you investigate?"
                ),
                "options": [
                    "Use cross-validation to assess stability across splits",
                    "Train only on the easiest split to improve the score",
                    "Remove the validation data so the result becomes stable",
                    "Increase the number of output labels without testing",
                ],
                "answer": "Use cross-validation to assess stability across splits",
                "skill": "Model validation",
                "difficulty": "Intermediate",
                "question_type": "Technical",
                "concept": "Cross-validation",
            },
            {
                "question": (
                    "A model's training loss keeps decreasing while validation "
                    "loss starts increasing. What does this pattern suggest?"
                ),
                "options": [
                    "The model is beginning to overfit the training data",
                    "The model has stopped learning from the training data",
                    "The validation set has become part of the training set",
                    "The model will necessarily improve on unseen production data",
                ],
                "answer": "The model is beginning to overfit the training data",
                "skill": "Deep learning",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "Validation loss",
            },
            {
                "question": (
                    "You need to deploy a trained model behind an API. Which "
                    "design is most appropriate for a production service?"
                ),
                "options": [
                    "Load the model once and expose controlled prediction endpoints",
                    "Retrain the model for every incoming API request",
                    "Store the model inside each user's browser session",
                    "Return the training dataset whenever a prediction is requested",
                ],
                "answer": "Load the model once and expose controlled prediction endpoints",
                "skill": "Model deployment",
                "difficulty": "Advanced",
                "question_type": "Decision Making",
                "concept": "Model serving",
            },
            {
                "question": (
                    "A deployed model's accuracy gradually decreases even though "
                    "the code has not changed. What should an AI engineer investigate?"
                ),
                "options": [
                    "Check for data drift and changes in real-world inputs",
                    "Delete the validation metrics because they are outdated",
                    "Assume the model is correct because the code is unchanged",
                    "Disable monitoring so production results appear more stable",
                ],
                "answer": "Check for data drift and changes in real-world inputs",
                "skill": "Model monitoring",
                "difficulty": "Advanced",
                "question_type": "Debugging",
                "concept": "Data drift",
            },
            {
                "question": (
                    "Two models have similar validation scores, but one is much "
                    "more complex and expensive to serve. What should guide the choice?"
                ),
                "options": [
                    "Compare accuracy with latency, cost, complexity, and requirements",
                    "Always choose the model with the most parameters",
                    "Always choose the model that took longest to train",
                    "Ignore deployment constraints because validation score is enough",
                ],
                "answer": "Compare accuracy with latency, cost, complexity, and requirements",
                "skill": "Model selection",
                "difficulty": "Advanced",
                "question_type": "Decision Making",
                "concept": "Model trade-offs",
            },
        ]

    # --------------------------------------------------------
    # DATA SCIENTIST
    # --------------------------------------------------------

    elif "data scientist" in role_lower:

        questions = [
            {
                "question": (
                    "Before building a predictive model, which action gives "
                    "the strongest understanding of a new dataset?"
                ),
                "options": [
                    "Inspect distributions, missing values, and relationships",
                    "Train the most complex model immediately",
                    "Remove all unusual records without investigation",
                    "Create predictions before checking the target variable",
                ],
                "answer": "Inspect distributions, missing values, and relationships",
                "skill": "Exploratory data analysis",
                "difficulty": "Foundation",
                "question_type": "Applied",
                "concept": "EDA",
            },
            {
                "question": (
                    "A feature has a very strong correlation with the target. "
                    "What should you conclude?"
                ),
                "options": [
                    "Investigate whether the relationship is meaningful and valid",
                    "Assume the feature proves a causal relationship",
                    "Remove every other feature because one feature is enough",
                    "Assume the model will always perform well in production",
                ],
                "answer": "Investigate whether the relationship is meaningful and valid",
                "skill": "Statistics",
                "difficulty": "Foundation",
                "question_type": "Scenario",
                "concept": "Correlation",
            },
            {
                "question": (
                    "A SQL query joins a customer table with an orders table and "
                    "suddenly returns many duplicate-looking customer rows. What "
                    "should you check first?"
                ),
                "options": [
                    "Check the join relationship and expected row cardinality",
                    "Delete all duplicate customers from the database",
                    "Add random values to the customer identifiers",
                    "Remove the orders table from the analysis",
                ],
                "answer": "Check the join relationship and expected row cardinality",
                "skill": "SQL",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "SQL joins",
            },
            {
                "question": (
                    "A dataset contains extreme values caused by measurement "
                    "errors. What is the best first response?"
                ),
                "options": [
                    "Investigate the source before deciding how to handle them",
                    "Always replace every extreme value with the mean",
                    "Always delete every row containing an extreme value",
                    "Ignore the values without checking their origin",
                ],
                "answer": "Investigate the source before deciding how to handle them",
                "skill": "Data cleaning",
                "difficulty": "Intermediate",
                "question_type": "Decision Making",
                "concept": "Outliers",
            },
            {
                "question": (
                    "You are predicting a rare event where missing a positive "
                    "case is much more costly than reviewing extra alerts. Which "
                    "metric deserves strong attention?"
                ),
                "options": [
                    "Recall because missing positive cases is especially costly",
                    "Accuracy because class frequency does not affect it",
                    "Training time because it directly measures business impact",
                    "Row count because more records always improve the metric",
                ],
                "answer": "Recall because missing positive cases is especially costly",
                "skill": "Model evaluation",
                "difficulty": "Intermediate",
                "question_type": "Scenario",
                "concept": "Recall",
            },
            {
                "question": (
                    "A dataset has a categorical feature with thousands of unique "
                    "values. Which approach should be considered carefully?"
                ),
                "options": [
                    "Choose an encoding strategy appropriate for high cardinality",
                    "Create thousands of unrelated binary features automatically",
                    "Delete the feature without checking its predictive value",
                    "Convert every category into the same constant value",
                ],
                "answer": "Choose an encoding strategy appropriate for high cardinality",
                "skill": "Feature engineering",
                "difficulty": "Intermediate",
                "question_type": "Decision Making",
                "concept": "Categorical encoding",
            },
            {
                "question": (
                    "A model has strong training performance but weak validation "
                    "performance. Which change should be investigated first?"
                ),
                "options": [
                    "Reduce overfitting through validation and model regularization",
                    "Increase training accuracy until validation becomes irrelevant",
                    "Remove the validation set so the model appears more consistent",
                    "Evaluate the model only on the same records used for training",
                ],
                "answer": "Reduce overfitting through validation and model regularization",
                "skill": "Machine learning",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "Generalization",
            },
            {
                "question": (
                    "A stakeholder says a model is accurate, but the model's "
                    "predictions are systematically worse for one important group. "
                    "What should you do?"
                ),
                "options": [
                    "Investigate subgroup performance and possible data or model issues",
                    "Ignore subgroup results because overall accuracy is higher",
                    "Remove the affected group from evaluation permanently",
                    "Report only the strongest metric to avoid confusion",
                ],
                "answer": "Investigate subgroup performance and possible data or model issues",
                "skill": "Model evaluation",
                "difficulty": "Advanced",
                "question_type": "Scenario",
                "concept": "Subgroup evaluation",
            },
            {
                "question": (
                    "A data pipeline calculates a feature using information that "
                    "would not exist at prediction time. What is the main concern?"
                ),
                "options": [
                    "The feature may cause leakage and inflate validation performance",
                    "The feature guarantees better production performance",
                    "The feature removes the need for a separate test dataset",
                    "The feature automatically makes the model more interpretable",
                ],
                "answer": "The feature may cause leakage and inflate validation performance",
                "skill": "Feature engineering",
                "difficulty": "Advanced",
                "question_type": "Debugging",
                "concept": "Data leakage",
            },
            {
                "question": (
                    "A business team asks why a model's prediction changed after "
                    "a new data pipeline was introduced. What should you compare?"
                ),
                "options": [
                    "Compare data distributions, transformations, and feature definitions",
                    "Compare only the model name because data changes cannot matter",
                    "Ignore the pipeline because trained models never depend on input data",
                    "Replace the model immediately without investigating the pipeline",
                ],
                "answer": "Compare data distributions, transformations, and feature definitions",
                "skill": "Data pipeline debugging",
                "difficulty": "Advanced",
                "question_type": "Debugging",
                "concept": "Pipeline consistency",
            },
        ]

    # --------------------------------------------------------
    # DATA ANALYST
    # --------------------------------------------------------

    elif "data analyst" in role_lower:

        questions = [
            {
                "question": (
                    "A business analyst receives a sales dataset with missing "
                    "values and inconsistent product names. What should happen first?"
                ),
                "options": [
                    "Profile the data and identify quality problems before analysis",
                    "Create charts immediately without checking the values",
                    "Delete every row containing any missing field",
                    "Replace every inconsistent name with a random label",
                ],
                "answer": "Profile the data and identify quality problems before analysis",
                "skill": "Data cleaning",
                "difficulty": "Foundation",
                "question_type": "Applied",
                "concept": "Data profiling",
            },
            {
                "question": (
                    "A dashboard shows revenue increasing while the number of "
                    "customers is decreasing. What is the best next step?"
                ),
                "options": [
                    "Investigate revenue per customer and other supporting metrics",
                    "Assume customer loss cannot affect revenue",
                    "Delete the customer metric because it conflicts with revenue",
                    "Conclude immediately that the business is performing perfectly",
                ],
                "answer": "Investigate revenue per customer and other supporting metrics",
                "skill": "Business metrics",
                "difficulty": "Foundation",
                "question_type": "Scenario",
                "concept": "Metric interpretation",
            },
            {
                "question": (
                    "A SQL query needs the total sales amount for each customer. "
                    "Which operation is most relevant?"
                ),
                "options": [
                    "Group sales by customer and calculate the required aggregate",
                    "Sort customers alphabetically without calculating totals",
                    "Join every customer to every order without a condition",
                    "Return only the first order for each customer",
                ],
                "answer": "Group sales by customer and calculate the required aggregate",
                "skill": "SQL",
                "difficulty": "Intermediate",
                "question_type": "Technical",
                "concept": "GROUP BY",
            },
            {
                "question": (
                    "A chart contains monthly sales values, but one month is much "
                    "higher than all others. What should an analyst do?"
                ),
                "options": [
                    "Investigate the cause before deciding how to interpret it",
                    "Remove the month automatically because it is unusual",
                    "Replace the value with the average without checking the source",
                    "Ignore the value because charts should contain similar points",
                ],
                "answer": "Investigate the cause before deciding how to interpret it",
                "skill": "Data interpretation",
                "difficulty": "Intermediate",
                "question_type": "Scenario",
                "concept": "Outlier investigation",
            },
            {
                "question": (
                    "A stakeholder wants to compare conversion rates across "
                    "marketing channels. Which metric is most appropriate?"
                ),
                "options": [
                    "Compare converted users relative to users exposed to each channel",
                    "Compare only the total number of clicks across all channels",
                    "Compare channel names alphabetically and rank them",
                    "Compare the largest revenue value without considering audience size",
                ],
                "answer": "Compare converted users relative to users exposed to each channel",
                "skill": "Business metrics",
                "difficulty": "Intermediate",
                "question_type": "Decision Making",
                "concept": "Conversion rate",
            },
            {
                "question": (
                    "A dashboard becomes slow after adding several visualizations. "
                    "What should you investigate first?"
                ),
                "options": [
                    "Check query performance, data volume, and unnecessary calculations",
                    "Add more charts because more visuals improve performance",
                    "Duplicate the dashboard so each copy loads the same data",
                    "Remove all filters because filtering always causes slow queries",
                ],
                "answer": "Check query performance, data volume, and unnecessary calculations",
                "skill": "Dashboard optimization",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "Dashboard performance",
            },
            {
                "question": (
                    "A manager asks whether an increase in advertising caused "
                    "sales to rise. What should an analyst avoid doing?"
                ),
                "options": [
                    "Claiming causation from correlation without suitable evidence",
                    "Checking whether the two variables move together",
                    "Examining other factors that could influence sales",
                    "Reviewing the period and population used for comparison",
                ],
                "answer": "Claiming causation from correlation without suitable evidence",
                "skill": "Statistics",
                "difficulty": "Intermediate",
                "question_type": "Scenario",
                "concept": "Correlation and causation",
            },
            {
                "question": (
                    "Two reports show different revenue totals for the same month. "
                    "What is the most useful debugging approach?"
                ),
                "options": [
                    "Compare filters, joins, date definitions, and aggregation logic",
                    "Choose the larger value because it looks more complete",
                    "Average the two values without checking their calculations",
                    "Delete one report so stakeholders see only one number",
                ],
                "answer": "Compare filters, joins, date definitions, and aggregation logic",
                "skill": "Analytical validation",
                "difficulty": "Advanced",
                "question_type": "Debugging",
                "concept": "Metric reconciliation",
            },
            {
                "question": (
                    "A dashboard is used by executives who need quick decisions. "
                    "Which design choice is most appropriate?"
                ),
                "options": [
                    "Prioritize relevant KPIs, clear trends, and concise explanations",
                    "Display every available column to avoid hiding information",
                    "Use as many colors and charts as possible for visual impact",
                    "Remove labels because experienced users should infer every metric",
                ],
                "answer": "Prioritize relevant KPIs, clear trends, and concise explanations",
                "skill": "Data visualization",
                "difficulty": "Advanced",
                "question_type": "Decision Making",
                "concept": "Dashboard design",
            },
            {
                "question": (
                    "A report shows a strong improvement after changing the "
                    "definition of a KPI. What should be communicated?"
                ),
                "options": [
                    "Explain the definition change before comparing the results",
                    "Present the new result as directly comparable without context",
                    "Hide the previous definition to simplify the report",
                    "Assume the KPI improved because the number became larger",
                ],
                "answer": "Explain the definition change before comparing the results",
                "skill": "Data storytelling",
                "difficulty": "Advanced",
                "question_type": "Scenario",
                "concept": "Metric definitions",
            },
        ]

    # --------------------------------------------------------
    # BACKEND DEVELOPER
    # --------------------------------------------------------

    elif "backend" in role_lower:

        questions = [
            {
                "question": (
                    "A backend endpoint receives data from a client. What should "
                    "the server do before using that data?"
                ),
                "options": [
                    "Validate the input against expected rules and types",
                    "Trust every field because clients are always reliable",
                    "Store the data before checking whether it is valid",
                    "Return the data directly without processing it",
                ],
                "answer": "Validate the input against expected rules and types",
                "skill": "Input validation",
                "difficulty": "Foundation",
                "question_type": "Applied",
                "concept": "Request validation",
            },
            {
                "question": (
                    "A REST API receives a request for a resource that does not "
                    "exist. Which response is generally appropriate?"
                ),
                "options": [
                    "Return a suitable not-found HTTP status",
                    "Return a successful response with unrelated data",
                    "Return server credentials in the response body",
                    "Create the resource silently without the client's request",
                ],
                "answer": "Return a suitable not-found HTTP status",
                "skill": "HTTP and REST APIs",
                "difficulty": "Foundation",
                "question_type": "Technical",
                "concept": "HTTP status codes",
            },
            {
                "question": (
                    "A database query becomes slow as the table grows. What should "
                    "you investigate before rewriting the entire application?"
                ),
                "options": [
                    "Inspect the query plan and consider suitable indexes",
                    "Delete older records without checking business requirements",
                    "Add random indexes to every column immediately",
                    "Move all database logic into frontend JavaScript",
                ],
                "answer": "Inspect the query plan and consider suitable indexes",
                "skill": "Database optimization",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "Database indexes",
            },
            {
                "question": (
                    "An authenticated user can access another user's private "
                    "resource by changing an ID in the URL. What is missing?"
                ),
                "options": [
                    "Authorization checks for ownership or permitted access",
                    "A larger database because IDs should never be visible",
                    "More frontend styling because URLs are part of the interface",
                    "A faster server because authorization only affects performance",
                ],
                "answer": "Authorization checks for ownership or permitted access",
                "skill": "Authorization",
                "difficulty": "Intermediate",
                "question_type": "Security",
                "concept": "Access control",
            },
            {
                "question": (
                    "An API occasionally fails because a downstream service is "
                    "temporarily unavailable. What is a useful design consideration?"
                ),
                "options": [
                    "Use controlled error handling and appropriate retry behavior",
                    "Expose internal exception details to every client",
                    "Retry forever until the downstream service responds",
                    "Ignore the failure and return successful fake data",
                ],
                "answer": "Use controlled error handling and appropriate retry behavior",
                "skill": "Error handling",
                "difficulty": "Intermediate",
                "question_type": "Scenario",
                "concept": "Service failures",
            },
            {
                "question": (
                    "A Django page becomes slow because it loads related database "
                    "objects inside a loop. What should you investigate?"
                ),
                "options": [
                    "Use suitable query optimization for related objects",
                    "Add more database queries inside the same loop",
                    "Move all database records into browser cookies",
                    "Disable database access logging without changing the query",
                ],
                "answer": "Use suitable query optimization for related objects",
                "skill": "Django database optimization",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "N+1 queries",
            },
            {
                "question": (
                    "A backend stores passwords directly in the database. What "
                    "should be changed?"
                ),
                "options": [
                    "Use a secure password hashing mechanism provided by the framework",
                    "Encrypt passwords with a reversible key stored beside them",
                    "Move passwords into frontend JavaScript variables",
                    "Store passwords in logs so they are easier to recover",
                ],
                "answer": "Use a secure password hashing mechanism provided by the framework",
                "skill": "Application security",
                "difficulty": "Intermediate",
                "question_type": "Security",
                "concept": "Password storage",
            },
            {
                "question": (
                    "An API is returning sensitive fields that the client does "
                    "not need. What is the best improvement?"
                ),
                "options": [
                    "Return only the fields required for the intended operation",
                    "Return every database field so clients have more information",
                    "Hide the fields only with CSS after sending them to the browser",
                    "Put sensitive fields into response headers for convenience",
                ],
                "answer": "Return only the fields required for the intended operation",
                "skill": "API security",
                "difficulty": "Advanced",
                "question_type": "Security",
                "concept": "Data exposure",
            },
            {
                "question": (
                    "An endpoint is receiving thousands of requests in a short "
                    "period and the server becomes overloaded. What should be considered?"
                ),
                "options": [
                    "Use rate limiting and investigate the source of the traffic",
                    "Increase database queries for every incoming request",
                    "Disable authentication so requests complete faster",
                    "Return successful responses without performing the requested work",
                ],
                "answer": "Use rate limiting and investigate the source of the traffic",
                "skill": "API protection",
                "difficulty": "Advanced",
                "question_type": "Decision Making",
                "concept": "Rate limiting",
            },
            {
                "question": (
                    "A production bug cannot be reproduced locally. Which approach "
                    "is most useful before making random code changes?"
                ),
                "options": [
                    "Inspect logs, inputs, environment differences, and failure patterns",
                    "Rewrite the affected module without collecting evidence",
                    "Disable production monitoring to remove confusing information",
                    "Change several unrelated components and deploy them together",
                ],
                "answer": "Inspect logs, inputs, environment differences, and failure patterns",
                "skill": "Backend debugging",
                "difficulty": "Advanced",
                "question_type": "Debugging",
                "concept": "Production debugging",
            },
        ]

    # --------------------------------------------------------
    # FULL STACK DEVELOPER
    # --------------------------------------------------------

    elif "full stack" in role_lower:

        questions = [
            {
                "question": (
                    "A web page contains a form that sends user data to a backend. "
                    "What should the frontend do before submission?"
                ),
                "options": [
                    "Validate basic input requirements and provide useful feedback",
                    "Assume the backend will accept every possible value",
                    "Store passwords in the page source before submission",
                    "Disable validation so every form submission succeeds",
                ],
                "answer": "Validate basic input requirements and provide useful feedback",
                "skill": "Frontend development",
                "difficulty": "Foundation",
                "question_type": "Applied",
                "concept": "Form validation",
            },
            {
                "question": (
                    "A frontend application needs data from a backend service. "
                    "Which mechanism is commonly used?"
                ),
                "options": [
                    "Send an HTTP request to an API endpoint",
                    "Read the backend database file directly from the browser",
                    "Copy the backend source code into the webpage",
                    "Store the server's database credentials in JavaScript",
                ],
                "answer": "Send an HTTP request to an API endpoint",
                "skill": "REST APIs",
                "difficulty": "Foundation",
                "question_type": "Technical",
                "concept": "Frontend-backend communication",
            },
            {
                "question": (
                    "A responsive page looks correct on a desktop but overflows "
                    "horizontally on a phone. What should you investigate?"
                ),
                "options": [
                    "Check responsive layout rules, widths, and overflowing elements",
                    "Increase every element's fixed width for consistency",
                    "Remove the mobile viewport setting from the page",
                    "Add more horizontal content so the overflow is expected",
                ],
                "answer": "Check responsive layout rules, widths, and overflowing elements",
                "skill": "Responsive design",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "Responsive layouts",
            },
            {
                "question": (
                    "A frontend fetch request returns a successful HTTP response "
                    "but the expected data is missing. What should you check?"
                ),
                "options": [
                    "Inspect the response structure and the code reading its fields",
                    "Assume the server returned exactly the expected object",
                    "Delete the API endpoint because successful responses cannot be wrong",
                    "Change the CSS because response data is controlled by styling",
                ],
                "answer": "Inspect the response structure and the code reading its fields",
                "skill": "JavaScript",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "API response handling",
            },
            {
                "question": (
                    "A user submits a form twice because the first request takes "
                    "several seconds. What frontend behavior can improve this?"
                ),
                "options": [
                    "Disable repeated submission while the request is being processed",
                    "Send additional requests until one returns quickly",
                    "Refresh the page repeatedly during every submission",
                    "Ignore duplicate requests because the backend always handles them",
                ],
                "answer": "Disable repeated submission while the request is being processed",
                "skill": "Frontend UX",
                "difficulty": "Intermediate",
                "question_type": "Scenario",
                "concept": "Request state",
            },
            {
                "question": (
                    "A backend endpoint requires authentication, but a frontend "
                    "request receives an unauthorized response. What should be checked?"
                ),
                "options": [
                    "Verify the authentication state and required request credentials",
                    "Disable backend authentication for the frontend",
                    "Expose the backend password inside the JavaScript bundle",
                    "Assume every API endpoint should accept anonymous requests",
                ],
                "answer": "Verify the authentication state and required request credentials",
                "skill": "Authentication",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "Authenticated requests",
            },
            {
                "question": (
                    "A database-backed page becomes slow after adding a new list "
                    "view. What should be investigated?"
                ),
                "options": [
                    "Check database queries, indexes, and unnecessary repeated lookups",
                    "Move the database into browser local storage immediately",
                    "Add more HTML elements to reduce backend processing",
                    "Disable error handling so database requests complete faster",
                ],
                "answer": "Check database queries, indexes, and unnecessary repeated lookups",
                "skill": "Database optimization",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "Database performance",
            },
            {
                "question": (
                    "A frontend displays user-generated text as raw HTML and an "
                    "attacker can inject unwanted markup. What is the main concern?"
                ),
                "options": [
                    "The application may be vulnerable to cross-site scripting",
                    "The database will automatically become normalized",
                    "The browser will automatically encrypt the injected content",
                    "The API will automatically reject every unsafe HTML fragment",
                ],
                "answer": "The application may be vulnerable to cross-site scripting",
                "skill": "Web security",
                "difficulty": "Advanced",
                "question_type": "Security",
                "concept": "XSS",
            },
            {
                "question": (
                    "A page loads slowly because it requests a large amount of "
                    "unused data from the backend. What is a good improvement?"
                ),
                "options": [
                    "Request only the data required for the current page or operation",
                    "Send the entire database to the browser for fewer requests",
                    "Duplicate the same API request to increase responsiveness",
                    "Disable network monitoring so the page appears faster",
                ],
                "answer": "Request only the data required for the current page or operation",
                "skill": "API design",
                "difficulty": "Advanced",
                "question_type": "Decision Making",
                "concept": "Efficient data fetching",
            },
            {
                "question": (
                    "A full-stack feature works locally but fails in production. "
                    "Which investigation is most useful?"
                ),
                "options": [
                    "Compare configuration, environment variables, dependencies, and logs",
                    "Rewrite the frontend without checking the production environment",
                    "Assume production hardware is always the only cause",
                    "Remove all environment-specific settings from the application",
                ],
                "answer": "Compare configuration, environment variables, dependencies, and logs",
                "skill": "Deployment debugging",
                "difficulty": "Advanced",
                "question_type": "Debugging",
                "concept": "Environment differences",
            },
        ]

    # --------------------------------------------------------
    # WEB DEVELOPER
    # --------------------------------------------------------

    elif "web developer" in role_lower:

        questions = [
            {
                "question": (
                    "Which HTML practice best improves the structure and "
                    "accessibility of a web page?"
                ),
                "options": [
                    "Use semantic elements that describe the page structure",
                    "Use div elements for every part of the page",
                    "Remove headings because visual styling is enough",
                    "Put all page content inside a single large paragraph",
                ],
                "answer": "Use semantic elements that describe the page structure",
                "skill": "HTML",
                "difficulty": "Foundation",
                "question_type": "Technical",
                "concept": "Semantic HTML",
            },
            {
                "question": (
                    "A CSS layout works on a wide monitor but breaks on smaller "
                    "screens. What should you investigate?"
                ),
                "options": [
                    "Check responsive layout rules and fixed-width elements",
                    "Increase all fixed widths to make the layout consistent",
                    "Remove the viewport configuration from the page",
                    "Add more content so the smaller screen becomes scrollable",
                ],
                "answer": "Check responsive layout rules and fixed-width elements",
                "skill": "Responsive design",
                "difficulty": "Foundation",
                "question_type": "Debugging",
                "concept": "Responsive CSS",
            },
            {
                "question": (
                    "A CSS Grid layout needs cards to automatically fit available "
                    "space while keeping reasonable minimum widths. Which approach is useful?"
                ),
                "options": [
                    "Use responsive grid sizing with suitable minimum track widths",
                    "Give every card an identical fixed width for every screen",
                    "Place every card at an absolute position manually",
                    "Use a single-column layout regardless of viewport size",
                ],
                "answer": "Use responsive grid sizing with suitable minimum track widths",
                "skill": "CSS Grid",
                "difficulty": "Intermediate",
                "question_type": "Applied",
                "concept": "Responsive grid",
            },
            {
                "question": (
                    "A JavaScript button click sometimes triggers the same action "
                    "twice. What should you investigate?"
                ),
                "options": [
                    "Check whether multiple event listeners are being registered",
                    "Add another event listener to make the click more reliable",
                    "Reload the browser after every click",
                    "Move all button code into CSS",
                ],
                "answer": "Check whether multiple event listeners are being registered",
                "skill": "JavaScript",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "Event listeners",
            },
            {
                "question": (
                    "A page fetches data asynchronously and needs to update the "
                    "interface after the response arrives. What should be handled?"
                ),
                "options": [
                    "Handle the promise result and update the relevant UI state",
                    "Block the browser until the server responds",
                    "Assume the response is available immediately after fetch starts",
                    "Reload the entire page after every API request",
                ],
                "answer": "Handle the promise result and update the relevant UI state",
                "skill": "JavaScript",
                "difficulty": "Intermediate",
                "question_type": "Applied",
                "concept": "Async requests",
            },
            {
                "question": (
                    "A form works with a mouse but keyboard users cannot reach "
                    "one important control. What should be investigated?"
                ),
                "options": [
                    "Check keyboard focus order and accessible interactive elements",
                    "Hide the control from keyboard users to simplify navigation",
                    "Replace the control with an image without alternative text",
                    "Disable keyboard navigation because mouse input is sufficient",
                ],
                "answer": "Check keyboard focus order and accessible interactive elements",
                "skill": "Accessibility",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "Keyboard accessibility",
            },
            {
                "question": (
                    "A page downloads several large images that are below the fold. "
                    "What optimization could help?"
                ),
                "options": [
                    "Use appropriate image sizing and lazy loading where suitable",
                    "Increase image resolution so browsers cache more bytes",
                    "Duplicate the images in HTML to improve loading speed",
                    "Convert every image into a larger uncompressed format",
                ],
                "answer": "Use appropriate image sizing and lazy loading where suitable",
                "skill": "Web performance",
                "difficulty": "Intermediate",
                "question_type": "Decision Making",
                "concept": "Image optimization",
            },
            {
                "question": (
                    "A web page displays user-provided text using an unsafe HTML "
                    "insertion method. What security risk should be considered?"
                ),
                "options": [
                    "Cross-site scripting through injected content",
                    "Database normalization through additional HTML nodes",
                    "Automatic browser encryption of user-provided content",
                    "Improved caching caused by dynamic HTML insertion",
                ],
                "answer": "Cross-site scripting through injected content",
                "skill": "Web security",
                "difficulty": "Advanced",
                "question_type": "Security",
                "concept": "XSS",
            },
            {
                "question": (
                    "A JavaScript application makes many identical API requests "
                    "when users rapidly interact with a search field. What can help?"
                ),
                "options": [
                    "Debounce requests so rapid input does not trigger every search",
                    "Send more requests so the latest result arrives sooner",
                    "Reload the page after every typed character",
                    "Disable the search field until the user stops typing forever",
                ],
                "answer": "Debounce requests so rapid input does not trigger every search",
                "skill": "JavaScript performance",
                "difficulty": "Advanced",
                "question_type": "Applied",
                "concept": "Debouncing",
            },
            {
                "question": (
                    "A site looks correct in one browser but behaves differently "
                    "in another. What should a developer do first?"
                ),
                "options": [
                    "Reproduce the issue and inspect browser-specific behavior systematically",
                    "Assume the browser with the issue is always incorrect",
                    "Remove the feature without checking the underlying cause",
                    "Add random CSS rules until both browsers appear similar",
                ],
                "answer": "Reproduce the issue and inspect browser-specific behavior systematically",
                "skill": "Browser debugging",
                "difficulty": "Advanced",
                "question_type": "Debugging",
                "concept": "Cross-browser compatibility",
            },
        ]

    # --------------------------------------------------------
    # SOFTWARE ENGINEER / SOFTWARE DEVELOPER
    # --------------------------------------------------------

    elif (
        "software engineer" in role_lower
        or "software developer" in role_lower
    ):

        questions = [
            {
                "question": (
                    "A function is becoming difficult to test because it performs "
                    "many unrelated operations. What is a useful improvement?"
                ),
                "options": [
                    "Separate responsibilities into smaller focused components",
                    "Add more unrelated logic to keep everything together",
                    "Remove tests because the function is already working",
                    "Duplicate the function for every caller",
                ],
                "answer": "Separate responsibilities into smaller focused components",
                "skill": "Software design",
                "difficulty": "Foundation",
                "question_type": "Decision Making",
                "concept": "Single responsibility",
            },
            {
                "question": (
                    "Which data structure is generally appropriate when you need "
                    "fast lookup by a unique key?"
                ),
                "options": [
                    "A hash-based map or dictionary",
                    "A queue that only supports ordered removal",
                    "A stack that only exposes the latest element",
                    "A plain text file searched from beginning to end",
                ],
                "answer": "A hash-based map or dictionary",
                "skill": "Data structures",
                "difficulty": "Foundation",
                "question_type": "Technical",
                "concept": "Hash maps",
            },
            {
                "question": (
                    "A program repeatedly searches a sorted list for values. "
                    "Which algorithm can reduce the search work?"
                ),
                "options": [
                    "Binary search by repeatedly dividing the search range",
                    "Linear search that always checks every element",
                    "Random search that chooses unrelated positions",
                    "Bubble sort that repeatedly swaps adjacent values",
                ],
                "answer": "Binary search by repeatedly dividing the search range",
                "skill": "Algorithms",
                "difficulty": "Intermediate",
                "question_type": "Technical",
                "concept": "Binary search",
            },
            {
                "question": (
                    "A service contains duplicated validation logic in several "
                    "places. What is a maintainability concern?"
                ),
                "options": [
                    "Changes may become inconsistent across duplicated implementations",
                    "Duplicated logic always makes applications execute faster",
                    "Repeated code automatically improves security",
                    "Duplicated validation removes the need for testing",
                ],
                "answer": "Changes may become inconsistent across duplicated implementations",
                "skill": "Code quality",
                "difficulty": "Intermediate",
                "question_type": "Scenario",
                "concept": "Code duplication",
            },
            {
                "question": (
                    "A production bug occurs only for a specific input. What is "
                    "the strongest first debugging approach?"
                ),
                "options": [
                    "Reproduce the input and isolate the smallest failing case",
                    "Rewrite the entire module before checking the input",
                    "Change several unrelated functions at the same time",
                    "Disable error reporting so the failure disappears",
                ],
                "answer": "Reproduce the input and isolate the smallest failing case",
                "skill": "Debugging",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "Bug isolation",
            },
            {
                "question": (
                    "A database query is executed once for every item in a large "
                    "collection. What problem might this create?"
                ),
                "options": [
                    "Excessive database round trips can hurt performance",
                    "More queries always guarantee faster application performance",
                    "The database automatically converts the queries into one operation",
                    "Repeated queries eliminate the need for indexes",
                ],
                "answer": "Excessive database round trips can hurt performance",
                "skill": "Database optimization",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "N+1 queries",
            },
            {
                "question": (
                    "A feature requires changing several modules. What is a good "
                    "software engineering practice before implementation?"
                ),
                "options": [
                    "Understand dependencies and define the expected behavior first",
                    "Modify every module immediately without checking dependencies",
                    "Avoid tests because multiple modules make testing unnecessary",
                    "Deploy each partial change without verifying integration",
                ],
                "answer": "Understand dependencies and define the expected behavior first",
                "skill": "Software engineering",
                "difficulty": "Intermediate",
                "question_type": "Decision Making",
                "concept": "Change planning",
            },
            {
                "question": (
                    "Two implementations meet the same requirement. One is faster "
                    "but much harder to maintain. What should influence the decision?"
                ),
                "options": [
                    "Balance performance, maintainability, complexity, and requirements",
                    "Always choose the implementation with the most complex code",
                    "Always choose the fastest code regardless of maintenance cost",
                    "Choose randomly because equivalent behavior makes all designs equal",
                ],
                "answer": "Balance performance, maintainability, complexity, and requirements",
                "skill": "Technical decision making",
                "difficulty": "Advanced",
                "question_type": "Decision Making",
                "concept": "Engineering trade-offs",
            },
            {
                "question": (
                    "A system handles increasing traffic poorly even though individual "
                    "requests are fast. What should an engineer investigate?"
                ),
                "options": [
                    "Identify shared bottlenecks, resource limits, and scaling behavior",
                    "Only optimize variable names because they control traffic capacity",
                    "Remove monitoring because traffic makes metrics unreliable",
                    "Increase application complexity without measuring bottlenecks",
                ],
                "answer": "Identify shared bottlenecks, resource limits, and scaling behavior",
                "skill": "System performance",
                "difficulty": "Advanced",
                "question_type": "Scenario",
                "concept": "Scalability",
            },
            {
                "question": (
                    "A team wants to merge a change that passes local tests but "
                    "has no review or integration verification. What is the main risk?"
                ),
                "options": [
                    "The change may introduce integration or maintainability problems",
                    "Local tests guarantee every production integration will work",
                    "Code review is unnecessary when a program compiles successfully",
                    "Integration testing can never find problems after local testing",
                ],
                "answer": "The change may introduce integration or maintainability problems",
                "skill": "Testing and collaboration",
                "difficulty": "Advanced",
                "question_type": "Decision Making",
                "concept": "Code review",
            },
        ]

    # --------------------------------------------------------
    # GENERAL ROLE
    # --------------------------------------------------------

    else:

        questions = [
            {
                "question": (
                    f"A {role} task has unclear success criteria. What should "
                    "you do before implementation?"
                ),
                "options": [
                    "Clarify requirements, constraints, and expected outcomes",
                    "Start implementation and decide the goal afterward",
                    "Copy an existing solution without checking its suitability",
                    "Avoid asking questions so the task finishes faster",
                ],
                "answer": "Clarify requirements, constraints, and expected outcomes",
                "skill": "Requirements analysis",
                "difficulty": "Foundation",
                "question_type": "Scenario",
                "concept": "Requirements",
            },
            {
                "question": (
                    f"A result from a {role} task looks incorrect. What is the "
                    "most useful first response?"
                ),
                "options": [
                    "Check inputs, assumptions, and evidence before changing the solution",
                    "Change several unrelated parts of the solution immediately",
                    "Ignore the result because unexpected outputs are normal",
                    "Publish the result before investigating the problem",
                ],
                "answer": "Check inputs, assumptions, and evidence before changing the solution",
                "skill": "Problem solving",
                "difficulty": "Foundation",
                "question_type": "Debugging",
                "concept": "Root cause analysis",
            },
            {
                "question": (
                    "A technical task depends on information from another team. "
                    "What is the best approach?"
                ),
                "options": [
                    "Clarify the dependency and expected information early",
                    "Continue without the dependency and assume the details",
                    "Hide the dependency until the deadline approaches",
                    "Replace the required information with unrelated data",
                ],
                "answer": "Clarify the dependency and expected information early",
                "skill": "Collaboration",
                "difficulty": "Intermediate",
                "question_type": "Scenario",
                "concept": "Dependencies",
            },
            {
                "question": (
                    "A solution works for normal input but fails for an unusual "
                    "case. What should you investigate?"
                ),
                "options": [
                    "Identify the edge case and define the expected behavior",
                    "Remove the unusual case from all future testing",
                    "Assume users will never provide unusual input",
                    "Hide the failure instead of investigating its cause",
                ],
                "answer": "Identify the edge case and define the expected behavior",
                "skill": "Problem solving",
                "difficulty": "Intermediate",
                "question_type": "Debugging",
                "concept": "Edge cases",
            },
            {
                "question": (
                    "A team has two technically valid approaches. What should "
                    "guide the final choice?"
                ),
                "options": [
                    "Compare requirements, risks, cost, maintainability, and trade-offs",
                    "Choose the approach with the most complicated implementation",
                    "Choose randomly because both approaches technically work",
                    "Always choose the newest technology regardless of requirements",
                ],
                "answer": "Compare requirements, risks, cost, maintainability, and trade-offs",
                "skill": "Technical judgment",
                "difficulty": "Intermediate",
                "question_type": "Decision Making",
                "concept": "Trade-offs",
            },
            {
                "question": (
                    "A completed task passes one manual test. What should happen "
                    "before considering it production-ready?"
                ),
                "options": [
                    "Verify important requirements and test relevant failure cases",
                    "Assume one successful test proves every case works",
                    "Remove error handling because the manual test passed",
                    "Deploy immediately and wait for users to discover problems",
                ],
                "answer": "Verify important requirements and test relevant failure cases",
                "skill": "Quality assurance",
                "difficulty": "Intermediate",
                "question_type": "Applied",
                "concept": "Testing",
            },
            {
                "question": (
                    "A sensitive value is required by an application. Where should "
                    "it normally be stored?"
                ),
                "options": [
                    "Use secure configuration rather than hard-coding the secret",
                    "Commit the secret into the public source repository",
                    "Place the secret inside visible frontend text",
                    "Send the secret to team members through public messages",
                ],
                "answer": "Use secure configuration rather than hard-coding the secret",
                "skill": "Security practice",
                "difficulty": "Intermediate",
                "question_type": "Security",
                "concept": "Secret management",
            },
            {
                "question": (
                    "A system begins failing after a new component is introduced. "
                    "What debugging strategy is most useful?"
                ),
                "options": [
                    "Compare the change, isolate the failure, and inspect relevant evidence",
                    "Rewrite every component because one change caused the issue",
                    "Disable monitoring so the system produces fewer errors",
                    "Ignore the new component and modify unrelated code first",
                ],
                "answer": "Compare the change, isolate the failure, and inspect relevant evidence",
                "skill": "Debugging",
                "difficulty": "Advanced",
                "question_type": "Debugging",
                "concept": "Regression analysis",
            },
            {
                "question": (
                    f"A {role} solution must work reliably as usage grows. What "
                    "should be evaluated before scaling it?"
                ),
                "options": [
                    "Identify bottlenecks, resource limits, and expected growth",
                    "Assume the existing design will scale without measurement",
                    "Add complexity without checking current performance",
                    "Remove monitoring because scaling makes measurements unnecessary",
                ],
                "answer": "Identify bottlenecks, resource limits, and expected growth",
                "skill": "System planning",
                "difficulty": "Advanced",
                "question_type": "Scenario",
                "concept": "Scalability",
            },
            {
                "question": (
                    "A team must choose between a quick workaround and a more "
                    "maintainable solution. What should be considered?"
                ),
                "options": [
                    "Compare immediate value with technical debt, risk, and future cost",
                    "Always choose the workaround because speed is everything",
                    "Always choose the complex solution regardless of project needs",
                    "Avoid documenting the decision because it may change later",
                ],
                "answer": "Compare immediate value with technical debt, risk, and future cost",
                "skill": "Technical decision making",
                "difficulty": "Advanced",
                "question_type": "Decision Making",
                "concept": "Technical debt",
            },
        ]

    for question in questions:
        question["role"] = role

    return questions


def _fallback_questions(roles):
    """
    Generate fallback questions separately for every selected role.

    Correct answers are shuffled into random positions.
    """

    questions = []

    for role in roles:

        role_questions = _fallback_questions_for_role(role)

        for question in role_questions:

            options = question.get("options", [])
            answer = question.get("answer")

            shuffled_options = options.copy()
            random.shuffle(shuffled_options)

            question["options"] = shuffled_options
            question["answer"] = answer

        questions.extend(role_questions)

    return {
        "questions": questions
    }


# ============================================================
# AI ASSESSMENT GENERATION
# ============================================================

def _get_role_competencies(role):
    """
    Return a suitable competency map for a role.

    Known roles use a predefined competency map.
    Custom roles receive a generic but practical competency map.
    """

    role_lower = role.strip().casefold()

    for role_name, competencies in ROLE_COMPETENCIES.items():

        if role_name in role_lower or role_lower in role_name:
            return competencies

    if "backend" in role_lower:
        return ROLE_COMPETENCIES["backend developer"]

    if "frontend" in role_lower:
        return ROLE_COMPETENCIES["web developer"]

    if "web" in role_lower:
        return ROLE_COMPETENCIES["web developer"]

    if "data" in role_lower:
        return [
            "data handling",
            "SQL",
            "data cleaning",
            "statistics",
            "analysis",
            "visualization",
            "problem solving",
            "interpretation",
            "reporting",
            "technical communication",
        ]

    if "ai" in role_lower or "ml" in role_lower:
        return ROLE_COMPETENCIES["ai engineer"]

    return [
        "role-specific fundamentals",
        "technical problem solving",
        "practical execution",
        "tools and workflows",
        "debugging",
        "quality assurance",
        "security",
        "technical decision making",
        "communication",
        "professional practice",
    ]


def _generate_questions_for_roles(roles):
    """
    Ask Ollama to generate questions for ALL selected roles
    in ONE request.

    Every role receives exactly 10 questions:

        2 Foundation
        5 Intermediate
        3 Advanced

    The correct answer position is randomized in Python
    after the AI response is validated.
    """

    total_questions = len(roles) * 10

    role_sections = []

    for index, role in enumerate(roles):

        competencies = _get_role_competencies(role)

        competency_text = "\n".join(
            f"- {item}"
            for item in competencies
        )

        role_sections.append(
            f"""
ROLE {index + 1}: {role}

REQUIRED COMPETENCIES:
{competency_text}
"""
        )

    role_list = "\n".join(role_sections)

    prompt = f"""
You are an expert technical assessment designer.

Create exactly {total_questions} multiple-choice questions for the
following target job roles.

{role_list}

============================================================
ASSESSMENT STRUCTURE
============================================================

Each role MUST receive exactly 10 questions:

- 2 Foundation
- 5 Intermediate
- 3 Advanced

The difficulty distribution MUST be exact for EVERY role.

============================================================
QUESTION QUALITY
============================================================

These are job-readiness assessments.

Questions must test practical understanding rather than memorization.

Prefer:

- realistic technical scenarios
- debugging situations
- interpreting results
- choosing between technical approaches
- practical implementation decisions
- workplace engineering situations
- tool and technology usage
- reasoning about trade-offs
- identifying problems in code, data, APIs, models, systems, or workflows

Avoid trivial questions such as:

"What is Python?"
"What is SQL?"
"What is HTML?"

Instead ask questions that require the student to APPLY the concept.

============================================================
FOUNDATION QUESTIONS
============================================================

Foundation questions should test essential role knowledge.

They must NOT be childish or obvious.

============================================================
INTERMEDIATE QUESTIONS
============================================================

Intermediate questions should involve practical application,
debugging, implementation, or technical decisions.

============================================================
ADVANCED QUESTIONS
============================================================

Advanced questions should involve:

- debugging
- interpreting behavior
- architecture decisions
- trade-offs
- performance
- reliability
- security
- realistic workplace scenarios

Do not use obscure trivia.

============================================================
ROLE RELEVANCE
============================================================

Every question must be strongly related to the exact target role.

Do NOT mix unrelated skills.

For example:

An AI Engineer question may involve:
Python, preprocessing, feature engineering, ML,
model evaluation, deployment, monitoring, etc.

A Data Analyst question may involve:
SQL, cleaning, visualization, metrics, interpretation,
dashboards, statistics, etc.

A Backend Developer question may involve:
APIs, HTTP, Django/frameworks, databases,
authentication, authorization, security, testing, etc.

============================================================
CONCEPT COVERAGE
============================================================

Avoid asking the same concept repeatedly.

Within each role, distribute questions across different competencies.

Every question MUST contain:

- role
- question
- exactly 4 options
- answer
- skill
- difficulty
- question_type
- concept

Allowed difficulty values:

Foundation
Intermediate
Advanced

Allowed question_type values:

Technical
Scenario
Debugging
Decision Making
Applied
Security

============================================================
ANSWER OPTIONS
============================================================

Every question must have exactly 4 plausible options.

IMPORTANT:

The correct answer must NOT be obviously longer than the other options.

All four options should have approximately similar length.

Avoid:

- one extremely detailed correct answer
- three short obviously wrong answers
- silly distractors
- joke answers
- "all of the above"
- "none of the above"
- impossible technical claims

Wrong answers should represent realistic mistakes,
misconceptions, or alternative approaches.

The correct answer should not always appear first.

The answer field MUST exactly match one option.

============================================================
IMPORTANT ANTI-BIAS RULE
============================================================

Do not make the correct answer recognizable simply because:

- it is longer
- it contains more technical terminology
- it sounds more professional
- it contains more explanation
- the other options are obviously simplistic

All options should look credible.

============================================================
OUTPUT
============================================================

Return JSON ONLY.

Use exactly this structure:

{{
    "questions": [
        {{
            "role": "Exact role name",
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Exact correct option",
            "skill": "Specific competency",
            "difficulty": "Foundation",
            "question_type": "Technical",
            "concept": "Specific concept"
        }}
    ]
}}

There must be exactly {total_questions} questions total.

There must be exactly 10 questions for EACH role.

Each role must contain exactly:

2 Foundation
5 Intermediate
3 Advanced

Return NO explanation outside the JSON.
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        raw_response = data.get(
            "response",
            ""
        )

        quiz = json.loads(
            raw_response
        )

        questions = quiz.get(
            "questions",
            []
        )

        # ----------------------------------------------------
        # BASIC VALIDATION
        # ----------------------------------------------------

        if not isinstance(
            questions,
            list
        ):
            return None

        if len(questions) != total_questions:
            return None

        validated = []

        role_counts = {
            role: 0
            for role in roles
        }

        difficulty_counts = {
            role: {
                "Foundation": 0,
                "Intermediate": 0,
                "Advanced": 0,
            }
            for role in roles
        }

        normalized_roles = {
            str(role).strip().casefold(): role
            for role in roles
        }

        # ----------------------------------------------------
        # VALIDATE EVERY QUESTION
        # ----------------------------------------------------

        for question in questions:

            if not isinstance(
                question,
                dict
            ):
                return None

            raw_role = str(
                question.get(
                    "role",
                    ""
                )
            ).strip()

            canonical_role = normalized_roles.get(
                raw_role.casefold()
            )

            if not canonical_role:
                return None

            text = str(
                question.get(
                    "question",
                    ""
                )
            ).strip()

            options = question.get(
                "options",
                []
            )

            answer = str(
                question.get(
                    "answer",
                    ""
                )
            ).strip()

            skill = str(
                question.get(
                    "skill",
                    ""
                )
            ).strip()

            difficulty = str(
                question.get(
                    "difficulty",
                    ""
                )
            ).strip()

            question_type = str(
                question.get(
                    "question_type",
                    ""
                )
            ).strip()

            concept = str(
                question.get(
                    "concept",
                    ""
                )
            ).strip()

            # ------------------------------------------------
            # REQUIRED FIELDS
            # ------------------------------------------------

            if not text:
                return None

            if not skill:
                return None

            if not concept:
                return None

            if not isinstance(
                options,
                list
            ):
                return None

            if len(options) != 4:
                return None

            if difficulty not in {
                "Foundation",
                "Intermediate",
                "Advanced",
            }:
                return None

            if question_type not in {
                "Technical",
                "Scenario",
                "Debugging",
                "Decision Making",
                "Applied",
                "Security",
            }:
                return None

            # ------------------------------------------------
            # CLEAN OPTIONS
            # ------------------------------------------------

            cleaned_options = [
                str(option).strip()
                for option in options
            ]

            if any(
                not option
                for option in cleaned_options
            ):
                return None

            # ------------------------------------------------
            # NO DUPLICATE OPTIONS
            # ------------------------------------------------

            normalized_options = {
                option.casefold()
                for option in cleaned_options
            }

            if len(
                normalized_options
            ) != 4:
                return None

            # ------------------------------------------------
            # CORRECT ANSWER MUST EXIST
            # ------------------------------------------------

            if answer not in cleaned_options:
                return None

            # ------------------------------------------------
            # OPTION LENGTH VALIDATION
            # ------------------------------------------------
            #
            # Prevent the correct answer from being much longer
            # than the distractors.
            #
            # This is deliberately not too strict because natural
            # language answers will never have exactly equal lengths.
            # ------------------------------------------------

            option_lengths = [
                len(option)
                for option in cleaned_options
            ]

            shortest_length = min(
                option_lengths
            )

            longest_length = max(
                option_lengths
            )

            if shortest_length > 0:

                if (
                    longest_length
                    > shortest_length * 2.2
                ):
                    return None

            incorrect_lengths = [
                len(option)
                for option in cleaned_options
                if option != answer
            ]

            if incorrect_lengths:

                average_incorrect_length = (
                    sum(incorrect_lengths)
                    / len(incorrect_lengths)
                )

                if (
                    len(answer)
                    > average_incorrect_length * 1.8
                ):
                    return None

            # ------------------------------------------------
            # COUNT ROLE
            # ------------------------------------------------

            role_counts[
                canonical_role
            ] += 1

            # ------------------------------------------------
            # COUNT DIFFICULTY
            # ------------------------------------------------

            difficulty_counts[
                canonical_role
            ][
                difficulty
            ] += 1

            # ------------------------------------------------
            # RANDOMIZE ANSWER POSITION
            # ------------------------------------------------

            shuffled_options = (
                cleaned_options.copy()
            )

            random.shuffle(
                shuffled_options
            )

            validated.append(
                {
                    "question": text,

                    "options": shuffled_options,

                    "answer": answer,

                    "skill": skill,

                    "role": canonical_role,

                    "difficulty": difficulty,

                    "question_type": question_type,

                    "concept": concept,
                }
            )

        # ----------------------------------------------------
        # EXACTLY 10 QUESTIONS PER ROLE
        # ----------------------------------------------------

        for role in roles:

            if role_counts.get(
                role,
                0
            ) != 10:

                return None

        # ----------------------------------------------------
        # EXACT DIFFICULTY DISTRIBUTION
        # ----------------------------------------------------

        for role in roles:

            counts = difficulty_counts[
                role
            ]

            if counts["Foundation"] != 2:
                return None

            if counts["Intermediate"] != 5:
                return None

            if counts["Advanced"] != 3:
                return None

        return validated

    except (
        requests.RequestException,
        ValueError,
        KeyError,
        TypeError,
        json.JSONDecodeError,
    ):

        return None


# ============================================================
# MAIN ASSESSMENT GENERATOR
# ============================================================

def generate_job_assessment(roles):
    """
    Generate a separate 10-question assessment for every role.

    Maximum:
        3 roles

    Example:

        roles = [
            "AI Engineer",
            "Data Scientist"
        ]

    Result:

        10 AI Engineer questions
        +
        10 Data Scientist questions

        = 20 total questions
    """

    # --------------------------------------------------------
    # CLEAN ROLES
    # --------------------------------------------------------

    roles = [
        str(role).strip()
        for role in roles
        if str(role).strip()
    ]

    # Remove duplicate roles while preserving order.
    unique_roles = []

    seen_roles = set()

    for role in roles:

        normalized = role.casefold()

        if normalized not in seen_roles:

            seen_roles.add(
                normalized
            )

            unique_roles.append(
                role
            )

    roles = unique_roles[:3]

    # --------------------------------------------------------
    # NO ROLES
    # --------------------------------------------------------

    if not roles:

        return {
            "questions": []
        }

    # --------------------------------------------------------
    # ONE OLLAMA REQUEST FOR ALL ROLES
    # --------------------------------------------------------

    all_questions = (
        _generate_questions_for_roles(
            roles
        )
    )

    # --------------------------------------------------------
    # FALLBACK IF OLLAMA FAILS
    # --------------------------------------------------------

    if all_questions is None:

        fallback = _fallback_questions(
            roles
        )

        all_questions = fallback.get(
            "questions",
            []
        )

    # --------------------------------------------------------
    # RETURN QUESTIONS
    # --------------------------------------------------------

    return {
        "questions": all_questions
    }


# ============================================================
# POST-ASSESSMENT ANALYSIS
# ============================================================

def analyze_performance(
    student,
    roles,
    answers,
    score,
    total
):
    """
    Create personalized, role-specific post-assessment analysis.

    Each selected role gets its own:

    - strengths
    - skill gaps
    - score
    - suitability
    - learning roadmap
    - AI explanation

    The student's profile is also supplied to the AI so that
    recommendations can take the student's current background
    into account.
    """

    role_analyses = {}

    # --------------------------------------------------------
    # STUDENT PROFILE
    # --------------------------------------------------------

    student_profile = {
        "education": getattr(
            student,
            "education",
            ""
        ) or "",

        "branch": getattr(
            student,
            "branch",
            ""
        ) or "",

        "year": getattr(
            student,
            "year",
            ""
        ) or "",

        "skills": getattr(
            student,
            "skills",
            ""
        ) or "",

        "interests": getattr(
            student,
            "interests",
            ""
        ) or "",

        "experience_level": (
            getattr(
                student,
                "experience_level",
                ""
            )
            or "Beginner"
        ),
    }

    # --------------------------------------------------------
    # ANALYSE EACH ROLE SEPARATELY
    # --------------------------------------------------------

    for role in roles:

        role_answers = [
            item
            for item in answers
            if str(
                item.get(
                    "role",
                    ""
                )
            ).strip().casefold()
            == str(
                role
            ).strip().casefold()
        ]

        # ----------------------------------------------------
        # ROLE SCORE
        # ----------------------------------------------------

        role_total = len(
            role_answers
        )

        role_correct = sum(
            1
            for item in role_answers
            if item.get("correct")
        )

        role_percentage = (
            round(
                (
                    role_correct
                    / role_total
                ) * 100
            )
            if role_total
            else 0
        )

        # ----------------------------------------------------
        # SUITABILITY
        # ----------------------------------------------------

        if role_percentage >= 80:
            suitability = "Excellent"

        elif role_percentage >= 65:
            suitability = "Strong"

        elif role_percentage >= 50:
            suitability = "Good"

        elif role_percentage >= 35:
            suitability = "Developing"

        else:
            suitability = "Needs Improvement"

        # ----------------------------------------------------
        # ROLE-SPECIFIC STRENGTHS
        # ----------------------------------------------------

        strengths = []

        for item in role_answers:

            if item.get("correct"):

                skill = str(
                    item.get(
                        "skill",
                        "Role competency"
                    )
                ).strip()

                if (
                    skill
                    and skill not in strengths
                ):
                    strengths.append(
                        skill
                    )

        # ----------------------------------------------------
        # ROLE-SPECIFIC GAPS
        # ----------------------------------------------------

        gaps = []

        for item in role_answers:

            if not item.get("correct"):

                skill = str(
                    item.get(
                        "skill",
                        "Role competency"
                    )
                ).strip()

                if (
                    skill
                    and skill not in gaps
                ):
                    gaps.append(
                        skill
                    )

        # ----------------------------------------------------
        # PERSONALIZED ROADMAP
        # ----------------------------------------------------

        roadmap = build_learning_roadmap(
            student,
            [role],
            gaps
        )

        # ----------------------------------------------------
        # AI ROLE-SPECIFIC ANALYSIS
        # ----------------------------------------------------

        prompt = f"""
You are an evidence-based career guidance assistant.

Analyse the student's readiness specifically for this role:

TARGET ROLE:
{role}

STUDENT PROFILE:
Education: {student_profile["education"] or "Not provided"}
Branch / Specialization: {student_profile["branch"] or "Not provided"}
Year: {student_profile["year"] or "Not provided"}
Current Skills: {student_profile["skills"] or "Not provided"}
Interests: {student_profile["interests"] or "Not provided"}
Experience Level: {student_profile["experience_level"]}

ASSESSMENT:
Score: {role_correct}/{role_total}
Percentage: {role_percentage}%

DEMONSTRATED STRENGTHS:
{", ".join(strengths) or "None identified"}

SKILL GAPS:
{", ".join(gaps) or "None identified"}

Write a concise but specific analysis for this student and this role.

Your response must contain these sections:

CURRENT ROLE READINESS
Explain what the assessment evidence says about the student's current readiness for {role}.

STRENGTH ANALYSIS
For each demonstrated strength, explain why that competency matters for {role}.
Do not merely repeat the skill name.

PRIORITY IMPROVEMENTS
For each skill gap, explain what the student should improve and why it matters for {role}.

READINESS STATEMENT
Give a realistic statement about the student's current level.
Do not claim that the student is guaranteed to get a job.

IMPORTANT RULES:
- Base conclusions primarily on assessment evidence.
- Do not invent qualifications.
- Do not say a particular degree is mandatory unless the information explicitly proves that.
- Do not make promises about employment or salary.
- Keep the advice practical and student-friendly.
"""

        try:

            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=90,
            )

            response.raise_for_status()

            ai_analysis = (
                response
                .json()
                .get(
                    "response",
                    ""
                )
                .strip()
            )

        except (
            requests.RequestException,
            ValueError,
            KeyError,
            TypeError,
        ):

            ai_analysis = (
                f"For the {role} role, your current assessment "
                f"score is {role_percentage}%. "
                f"Your demonstrated strengths include "
                f"{', '.join(strengths) or 'no clearly demonstrated competencies yet'}. "
                f"The main areas to improve are "
                f"{', '.join(gaps) or 'no major gaps identified'}. "
                f"Use the learning roadmap to strengthen the "
                f"identified competencies through structured learning "
                f"and practical projects."
            )

        # ----------------------------------------------------
        # STORE ROLE ANALYSIS
        # ----------------------------------------------------

        role_analyses[role] = {
            "score": role_correct,
            "total": role_total,
            "percentage": role_percentage,
            "suitability": suitability,
            "strengths": strengths,
            "skill_gaps": gaps,
            "analysis": ai_analysis,
            "roadmap": roadmap,
        }

    # --------------------------------------------------------
    # FIND BEST CURRENT ROLE
    # --------------------------------------------------------

    best_match = None

    if role_analyses:

        best_role = max(
            role_analyses,
            key=lambda name: (
                role_analyses[name][
                    "percentage"
                ]
            ),
        )

        best_match = {
            "role": best_role,
            "score": role_analyses[
                best_role
            ]["score"],
            "total": role_analyses[
                best_role
            ]["total"],
            "percentage": role_analyses[
                best_role
            ]["percentage"],
            "suitability": role_analyses[
                best_role
            ]["suitability"],
        }

    # --------------------------------------------------------
    # OVERALL STRENGTHS
    # --------------------------------------------------------

    all_strengths = []

    for data in role_analyses.values():

        for skill in data["strengths"]:

            if skill not in all_strengths:
                all_strengths.append(
                    skill
                )

    # --------------------------------------------------------
    # OVERALL GAPS
    # --------------------------------------------------------

    all_gaps = []

    for data in role_analyses.values():

        for skill in data["skill_gaps"]:

            if skill not in all_gaps:
                all_gaps.append(
                    skill
                )

    # --------------------------------------------------------
    # BACKWARD COMPATIBILITY
    # --------------------------------------------------------

    combined_roadmap = []

    for role in roles:

        role_data = role_analyses.get(
            role
        )

        if role_data:

            combined_roadmap.extend(
                role_data["roadmap"]
            )

    # --------------------------------------------------------
    # RETURN COMPLETE ANALYSIS
    # --------------------------------------------------------

    return {
        "strengths": all_strengths,

        "skill_gaps": all_gaps,

        "summary": (
            "Your assessment has been analysed separately "
            "for each selected role. Review each role's "
            "strengths, skill gaps and learning roadmap "
            "to understand where you currently fit best "
            "and what to improve next."
        ),

        "roadmap": combined_roadmap,

        "role_analyses": role_analyses,

        "roadmaps_by_role": {
            role: data["roadmap"]
            for role, data in role_analyses.items()
        },

        "best_match": best_match,
    }