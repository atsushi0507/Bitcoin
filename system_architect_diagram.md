```plantuml
@startuml
skinparam linetype ortho
skinparam componentStyle rectangle

actor User

package "CryptoCompare API" {
  [CryptoCompare API] as API
}

package "Google BigQuery" {
  [BigQuery] as DBv}

package "Web Application" {
  [Streamlit Frontend] as FE
  [Backend Logic] as BE
  [Plotly Graphs] as Graphs
}

User --> FE : Get Price Data
FE --> BE : Request Data
BE --> API : Fetch 1-min Data
API --> BE : Return Data
BE --> DB : Query for Existing Timestamp
DB --> BE : Return Result
BE --> DB : Insert New Data (if no match)
BE --> DB : Save Data
FE --> BE : Request Data for Visualization
BE --> DB : Fetch Data
DB --> BE : Return Data
BE --> Graphs : Generate Trends and Graphs
Graphs --> FE : Display Interactive Graphs

@enduml
```