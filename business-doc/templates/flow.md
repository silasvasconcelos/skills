<!-- _header.md at the top -->

# Flows — <feature>

> All diagrams use **business language**. No technical names in default mode.

## Main flow — <process name>

```mermaid
flowchart TD
    Start([Customer starts <action>]) --> Validate{Validate data}
    Validate -->|ok| Process[Process order]
    Validate -->|invalid| Error[Notify customer]
    Process --> Approve{Requires approval?}
    Approve -->|yes| Wait[Wait for approver]
    Approve -->|no| Complete([Completed])
    Wait --> Complete
    Error --> End([End])
    Complete --> End
```

## Lifecycle — <entity>

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Submitted
    Submitted --> UnderReview
    UnderReview --> Approved
    UnderReview --> Rejected
    Approved --> Completed
    Rejected --> [*]
    Completed --> [*]
```

## User journey

```mermaid
journey
    title Journey of <persona>
    section Discovery
      Accesses system: 4: Persona
    section Execution
      Fills in data: 3: Persona
      Receives confirmation: 5: Persona
```

## Interaction with external systems

```mermaid
sequenceDiagram
    participant U as User
    participant S as System
    participant E as External system (purpose)
    U->>S: Requests <action>
    S->>E: Queries <data>
    E-->>S: Returns <data>
    S-->>U: Confirms result
```

## Decisions and exceptions
- Decision 1: ...
- Exception 1: ...
