#!/usr/bin/python
import random

# population - 20 decks
pop_size = 20

# each gene - 1 card
# here is a list of 100 cards to start each card has name/type/(cost/production)
# ok, only 49 to start. I got tired of typing
gene_list = [
("Forest", 1, "G"),("Swamp", 1, "B"),("Island", 1, "U"),("Mountain", 1, "R"),("Plains", 1, "W"),
("Lightning Bolt", 2, "R"), ("Blodcrazed Goblin", 2, "R"), ("Goblin Balloon Brigade", 2, "R"), 
("Incite", 2, "R"), ("Reverberate", 2, "R R"), ("Ember Hauler", 2, "R R"), ("Thunder Strike", 2, "1 R"),
("Goblin Piker", 2, "1 R"), ("Combust", 2, "1 R"), ("Fiery Hellhound", 2, "1 R R"), 
("Ancient Hellkite", 2, "4 R R R"), ("Cyclops Gladiator", 2, "1 R R R"), ("Magma Phoenix", 2, "3 R R"), 
("Destructive Force", 2, "5 R R"), ("Chandra's Outrage", 2, "2 R R"), ("Inferno Titan", 2, "4 R R"), 
("Chandra's Spitfire", 2, "2 R"), 
("Acidic Slime", 2, "3 G G"), ("Autumn's Veil", 2, "G"), ("Awakener Druid", 2, "2 G"),
("Back to Nature", 2, "1 G"), ("Llanowar Elves", 2, "G"), ("Birds of Paradise", 2, "G"),
("Brindle Board", 2, "2 G"), ("Cudgel Troll", 2, "2 G G"), ("Runeclaw Bear", 2, "1 G"),
("Giant Growth", 2, "G"), ("Giant Spider", 2, "3 G"), ("Cultivate", 2, "2 G"), ("Dryad's Favor", 2, "G"),
("Duskdale Wurm", 2, "5 G G"), ("Elvish Archdruid", 2, "1 G G"), ("Fauna Shaman", 2, "1 G"),
("Fog", 2, "G"),
("Angel's Feather", 2, "2"), ("Battle Effigy", 2, "1"), ("Crystal Ball", 2, "3"), ("Demon's Horn", 2, "2"),
("Dragon's Claw", 2, "2"), ("Elixir of Immortality", 2, "1"), ("Gargoyle Sentinel", 2, "3"),
("Jinxed Idol", 2, "2"), ("Juggernaut", 2, "4"), ("Kraken's Eye", 2, "2")
]

# each chromosome - deck of 20 cards
chrom_size = 20

# - read text file to generate list of 20 random cards (land/spells)?
# start by pulling a random pile from the genelist
def create_chromosome(size):
   deck = []
   for i in range(size):  
      deck.append(gene_list[random.randint(0, len(gene_list) - 1)])

   return deck

# fitness - number of turns that a spell can be successfully cast
# perfect fit - spell cast all 13 turns
def fitness(chrom):
   return (play_deck(chrom[1]), chrom[1])

def play_deck(deck):
   random.shuffle(deck)

   num_turns = 0

   hand = deck[0:7]
   deck = deck[7:]
   graveyard = []
   exile = []
   battlefield = []
   played = True

   while (len(deck) > 0):
      (hand, deck, graveyard, exile, battlefield, played) = play_turn(hand, deck, graveyard, exile, battlefield)

      print hand
      print battlefield
      
      num_turns = num_turns + 1
      if (not played): 
         break

   return num_turns

def mana_calc(battlefield):
   mana = ""

   for i in range(len(battlefield)):
      if (battlefield[i][1] == 1):
         mana = mana + battlefield[i][2]
   return mana   

def test_mana_calc():
   battlefield = []
   # set some cards in the battlefield
   for i in range(20):
      battlefield.append(gene_list[random.randint(0, len(gene_list) - 1)])  
   
   print battlefield
   print mana_calc(battlefield)

####################
def is_castable(card, available_mana):
   mana_cost = card[2].split(" ")
    
   converted_mana = []
   for i in range(len(mana_cost)):
      if mana_cost[i].isdigit():
         converted_mana.append(mana_cost[i])
      else:
         pos = available_mana.find(mana_cost[i])
   
         if (pos >= 0):
            available_mana = available_mana[0:pos] + available_mana[pos+1:]
         else:
            return False

   for i in range(len(converted_mana)):
      if (len(available_mana) - 1) < int(converted_mana[i]):
         return False 
      else:
         available_mana = available_mana[int(converted_mana[i]):] 
   
   return True

def cast_hand_card(hand, battlefield, available_mana):

   for i in range(len(hand)):
      if hand[i][1] == 2 and is_castable(hand[i], available_mana):
         battlefield.append(hand[i])
         hand = hand[0:i] + hand[i+1:]
         
         print "Hand after casting: %r " % (hand,)
         print "Bord after casting: %r " % (battlefield,)
         break

   return (hand, battlefield, available_mana)

def test_is_castable():
   is_castable(gene_list[random.randint(0, len(gene_list) - 1)], "BUWGR")

############################

def play_turn(hand, deck, graveyard, exile, battlefield):
   played = False

   # draw card
   hand.append(deck[0:1][0])
   deck = deck[1:]

   # check battlefield to see how much mana is available
   available_mana = mana_calc(battlefield)

   print "Available mana: " + available_mana

   print "Current Hand: %r" % (hand,)
   # cast a card in hand if possible
   (hand, battlefield, available_mana) = cast_hand_card(hand, battlefield, available_mana)

   # otherwise, play a land to move closer to casting a card in hand 
   # cast a card in hand if possible
       
   return (hand, deck, graveyard, exile, battlefield, played)

def rank_population(pop):
   for i in range(len(pop)):
      pop[i] = fitness(pop[i])

   return pop.sort()

# crossover - basic one point crossover
crossover_rate = .8
def crossover(x,y):
   pos = random.randint(0, chrom_size - 1)
   tempx = x[0:pos] + y[pos:]
   tempy = y[0:pos] + x[pos:]
 
   return x, y 

# mutation - swap a random card from the deck with a card from the genelist
mutationRate = .25
def mutation(chrom):
   pos = random.randint(0, chrom_size - 1)
   chrom[pos] = gene_list[random.randint(0, len(gene_list - 1))]

   return chrom

# elitism - keep the top 10% of decks as is - carry them forward without change to the next generation
elitism = .1

def main():
   #each item in population has a fitness value and a deck list (chromosome)
   population = []
   for i in range(pop_size):
      population.append((0, create_chromosome(chrom_size)))

   rank_population(population)

   while (population[0][0] != 13):
      rank_population(population)

# test_mana_calc()
# test_is_castable()

main()