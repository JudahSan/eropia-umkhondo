Vibe Coding 101
=

Thinking, Frameworks, Checkpoints, Debugging, Context


Thinking
-

- Logical: What is the game?
- Analytical: How do I play the game?
- Computational: What are the patterns behind the game?
- Procedural: How do I excel at the game?

Frameworks
-

- You don't know what you don't know
- How do I do the thing I want to?
- What frameworks
    - ...allow me to do that thing?
    - ...work best with LLMs?
- If you don't know... just ask!

Checkpoints/ versions
-

- Things break - this is a fact
- You should use version control (or checkpoints in Replit) to minimize this
- We'll chunk up out builds and move quickly in short sprints

Debugging
-

- It's actually a bit boring
    - But you can make anything fun
    - The best debugging is methodical and thorough

- Goals:
    - Understand how you app works
    - Understand where the error is

- How can you get to the root?
- How can you tell the LLM what's wrong?


Context
-

What do we mean when we say "context?"

Context window: the amount of tokens an LLM can process at a given time.

Context can be the prompt we provide to the LLM, but it can also be other things:

- Images
- Documentation
- Errors
- Details about your app/ environment/ preferences (!)

Because LLMs might have outdate training data (or lack details of our implementations),  we need to provide additional context.

Getting to a MVP
=

- Give AI only the info relevant to the MVP
- Start small and work up
- Provide foundational context and important details

Implement new features
-

- Provide context relevant to the new feature
- Mention frameworks, provide documentation with EXPLICIT details on implementation
- Make incremental changes (checkpoint)

Debugging errors
-

- Figure out how things work
- Figure out what's wrong
- Figure out how to get information to the LLM to get unstuch
    - Figure out how to direct context

MVP/Feature -> Test -> Error -> Debug -> Checkpoint
