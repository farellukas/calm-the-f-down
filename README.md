# calm-the-f-down
## Inspiration
While taking summer classes this year, we realized how difficult it is to manage and complete different tasks in a condensed period of time. We realize that the presence of stress did not make it any better in completing these tasks. This leads to the main problem calm the f(ood) down is trying to tackle: stress. Stress is such a big obstacle in everyone's life, whether it is during school or working or even playing a game, we all face stress, and usually it will only lead to poor judgement, decision-making, and overall productivity. With stress playing such a big role in impacting humans' regular life, we wanted to make a program that allows us to better control and overcome stress.

## What it does
calm the f(ood) down is a simple 2d cooking game that involves customer making orders where the player, as the chef, will then have to prepare the necessary ingredients, cook said ingredients, and finally serve them to the customer. While most games use a life system or a timer for the losing condition, the catch in calm the f(ood) down is that the player will lose once they reach a certain stress level threshold. Thus, the point of this game is to learn how to manage stress in an otherwise stressful game.

## How we built it
We built calm the f(ood) down using pygame as the game engine. We first figured out how to collect EEG data from the Muse 2. We then transformed the collected time-based data into frequency-based data which we then process to get the delta, theta, alpha, beta, gamma bands with frequency bands of 0-4, 4-8, 12-35, >35 Hz respectively. We settled on using the theta/beta ratio as a measurement of stress level. We then began working on the actual game, creating the walls, players, food, and finally interactions between those elements. We finally connected the theta/beta ration with the game itself.

## Challenges we ran into
We ran into multiple challenges while making this project:
1. Figuring out how to measure stress level since stress was not really a quantifiable property. However, we settled on theta/beta ratio as it was the simplest to implement yet still proven by research to be a relatively accurate measurement of stress. Other alternatives include measuring heart rate variability.
2. Finding a way to make the player collide with free-standing walls. We ultimately figured using sprites was a very easy solution but we were stuck at this stage for quite some time.

## Accomplishments that we're proud of
We were proud of being able to make a complete playable game and a functioning stress quantifier.

## What we learned
1. Deeper understanding of pygame
2. basic numpy usage
3. How the brain works
4. EEG
5. Transforming EEG data

## What's next for calm the f(ood) down
We hope to also be able to incorporate heart rate variability into our stress level measurement system to provide more accurate results. We also want to add sounds and other factors into the game that could help induce stress so that the player can learn to control greater stress stimuli. We also hope to develop the game more, adding more maps and/or random map generations and more ingredients with a cleaner and more interactive UI.
