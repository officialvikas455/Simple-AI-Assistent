
import chromadb

# 1. Initialize ChromaDB
chroma = chromadb.Client()

# 2. Create or get collection
zorvex_collection = chroma.get_or_create_collection(
    name="zorvex_collection"
)

# 3. Prepare documents
documents = [
    {
        "id": "leave_maternity",
        "category": "leave_policy",
        "title": "Maternity Leave",
        "content": """
        Maternity Leave Policy:
        Employees are eligible for 26 weeks of paid leave
        for the first two children and 12 weeks for the
        third child.

        Leave can be availed in one go or multiple spells.
        The policy states that leave can be availed by
        the mother or father. Verify this eligibility
        wording against the official HR policy.
        """
    },
    {
        "id": "leave_paternity",
        "category": "leave_policy",
        "title": "Paternity Leave",
        "content": """
        Paternity Leave Policy:
        Employees are eligible for 15 days of paid leave
        for the first two children and 7 days for the
        third child.

        This leave can be availed by the father of the
        child in one go or multiple spells.
        """
    },
    {
        "id": "leave_sick",
        "category": "leave_policy",
        "title": "Sick Leave",
        "content": """
        Sick Leave Policy:
        Employees receive 12 days of paid sick leave
        per year.

        Leave can be used for the employee's own illness
        or the illness of a family member.
        Leave can be taken in one go or multiple spells.
        """
    },
    {
        "id": "leave_casual",
        "category": "leave_policy",
        "title": "Casual Leave",
        "content": """
        Casual Leave Policy:
        Employees receive 12 days of paid casual leave
        per year for personal reasons.
        Leave can be taken in one go or multiple spells.
        """
    },
    {
        "id": "leave_earned",
        "category": "leave_policy",
        "title": "Earned Leave",
        "content": """
        Earned Leave Policy:
        Employees receive 30 days of paid earned leave
        per year for personal reasons.
        Leave can be taken in one go or multiple spells.
        """
    },
    {
        "id": "medical_policy",
        "category": "medical_policy",
        "title": "Medical Insurance and Reimbursement",
        "content": """
        Medical Policy:
        Covers employee medical benefits, health insurance,
        hospitalization, medical claims, reimbursement
        procedures, eligible expenses, dependent coverage
        and claim submission.
        """
    },
    {
        "id": "travel_expense",
        "category": "travel_expense",
        "title": "Travel and Expense Policy",
        "content": """
        Travel and Expense Policy:
        Covers official business travel, travel approval,
        flight and train bookings, hotel accommodation,
        food allowances, local transportation, expense
        reimbursement and supporting bill requirements.
        """
    },
    {
        "id": "tech_docs",
        "category": "tech_docs",
        "title": "Technical Documentation",
        "content": """
        Technical Documentation:
        Covers technical architecture, APIs, Python
        applications, databases, authentication, deployment,
        configuration, troubleshooting, integrations
        and development guidelines.
        """
    }
]

# 4. Insert documents into ChromaDB
zorvex_collection.upsert(
    ids=[doc["id"] for doc in documents],

    documents=[
        doc["title"] + "\n" + doc["content"]
        for doc in documents
    ],

    metadatas=[
        {
            "category": doc["category"],
            "title": doc["title"],
            "source": "company_documentation"
        }
        for doc in documents
    ]
)

print("Successfully added documents!")

# 5. Check total documents
print("Total documents:",
      zorvex_collection.count())



# Semantic search
results = zorvex_collection.query(
    query_texts=[
        "How many days of maternity leave are available?"
    ],
    n_results=1
)

for document in results["documents"][0]:
    print(document)
