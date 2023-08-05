**Welcome to ***YOUR DUMB*****

I have created a Wordle clone that runs in the terminal but with an intriguing twist.

In a traditional game of Wordle, players aim to guess a five-letter word within a limited number of attempts by submitting their guesses.

In my version, titled “YOUR DUMB” (more on that later…), players not only strive to guess the correct word but also have the opportunity to earn points based on the accuracy of each guess. For each character position that is guessed correctly, players earn 5 points. If a character is correctly identified but in the incorrect position, players earn 2 points. These points then serve as an in-game currency to unlock useful power-ups.

The game play is also integrated with OpenAI’s API. The implementation of OpenAI’s GPT models allows for a unique five-letter word to be dynamically generated each game, ensuring endless possibilities. Additionally, every user-submitted guess is validated by GPT to ensure each guess is a real, five-letter, English word that exists in the dictionary.

Throughout the player’s experience, they will also be routinely mocked with comments about their cognitive abilities. These sarcastic quips are displayed at different points throughout the game and are dynamically updated based on various user-specific parameters. Factors that influence these snarky remarks include whether it's the user's first game, if the user has a specific loss percentage, or in instances where the user submits a misspelled word or inputs an invalid guess. These disses are intended to add a layer of light hearted humor to the game and hopefully get a chuckle out of at least one person.

**Paste your openAI API key in a .env file inside the utils folder**