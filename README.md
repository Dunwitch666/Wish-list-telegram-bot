<h1>Wishlist Bot✨</h1>

<h3>Description</h3>
<p>This bot was created so that everyone can leave their gift wishes in it and share them with their friends!</p>
<p>What distinguishes it from analogs is that the bot works entirely through messages in the messenger itself, without using a mini-app, which makes it easier to use.</p>

<h3>How it works</h3>
<p>To understand how the bot works, I created something like an activity diagram.</p>

```mermaid
flowchart TD
    Start(Start) --> A[Bot greeting]
    A --> B{What to do?}

    B --> |My wishlist| C[Get my gifts from DB]
    B --> |Friend's wishlist| D[Enter friend's username]
    B --> |Create gift| K[Enter gift text]
    B --> |Close wishlist| L[Enter code word]
    B --> |Delete gift| AA[Show my gifts]

    AA --> AB[Enter id of the gift to delete]
    AB --> AC[Delete gift]
    AC --> End

    C --> M[Show list of gifts]

    K --> R[Send image]
    R --> T["Message: gift added"]

    L --> U[Save code word to DB]
    U --> V["Message: wishlist closed"]

    D --> X{User found?}
    X --> |No| Y["Message: user not found"]
    X --> |Yes| E{Is wishlist closed?}

    E --> |No| F[Show list of gifts]
    E --> |Yes| J[Enter code word]

    J --> W{"Is «Cancel» pressed?"}
    W --> |Yes| B
    W --> |No| H{Is the word correct?}
    H --> |Yes| F
    H --> |No| J

    M --> End(End)
    T --> End
    V --> End
    Y --> End
    F --> End
```

<h3>Stack</h3>
<ul>
  <li>python v3.13</li>
  <li>python-telegram-bot v22.5</li>
  <li>postgreSQL v18.6</li>
  <li>psycopg2</li>
</ul>