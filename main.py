from bakery import assert_equal
from drafter import *
from dataclasses import dataclass
from random import randint

set_website_title("Your Drafter Website")
set_site_information(
    "author",
    """
Your description can go here.
""",
    [],
    [],
    [],
)


@dataclass
class Rules:
    title: str
    description: str
    is_on: bool
    card_played: str
    card_below: str


@dataclass
class Card:
    number: int


@dataclass
class State:
    total_rules: int
    game_ruleset: list[Rules]
    last_card_played: str
    player_card_hand: list[Card]
    dealer_card_hand: list[Card]


@route
def index(state: State) -> Page:
    return Page(
        state,
        content = [
        "Mao but worse",
        "Welcome to the Start Page",
        Button("Start Game", "/start")
    ])


@route
def start(state: State) -> Page:
    state.player_card_hand = gen_player_hand()
    state.dealer_card_hand = gen_dealer_hand()
    return start_game_round(state)


@route
def start_game_round(state: State) -> Page:
    card_obj = state.player_card_hand[0]
    card_value = str(card_obj.number)
    if card_value == "11":
        display = "J"
    elif card_value == "12":
        display = "Q"
    elif card_value == "13":
        display = "K"
    else:
        display = card_value

    return Page(state, [
        "Last card played was " + state.last_card_played,
        "You are playing " + display,
        "Type the rule that applies. If no rule applies, type 'none'",
        TextBox("rule"),
        Button("Submit", "/player_plays")
    ])


@route
def player_plays(state: State, rule: str) -> Page:
    current_card = str(state.player_card_hand[0].number)
    state.last_card_played = current_card
    matched_rule = rule_filtered(state, current_card)
    if rule.lower().strip() == "none":
        if matched_rule.title == "none":
            return player_succeed(state)
        else:
            return player_punished(state, matched_rule)


    if matched_rule.title != "none" and rule.strip() == matched_rule.title:
        return player_succeed(state)
    else:
        return player_punished(state, matched_rule)



def rule_filtered(state: State, card_played: str) -> Rules:
    last = state.last_card_played
    for rule in state.game_ruleset:
        above = rule.card_played.split(",")
        below = rule.card_below.split(",")

        if card_played in above and last in below:
            return rule

    return Rules("none", "", True, "", "")



@route
def player_punished(state: State, rule: Rules) -> Page:
    if len(state.dealer_card_hand) > 1:
        card = state.dealer_card_hand.pop(0)
        state.player_card_hand.append(card)

        return Page(state, [
            Header("You were punished!"),
            Text("The rule you should have played was:"),
            Header(rule.title, 2),
            Text(rule.description),
            Button("Continue", "/start_game_round")
        ])
    else:
        return Page(
            state,
            [
                Header("You've Lost."),
                Header("The rule was:", 2),
                Header(rule.title, 3),
                Text(rule.description)
            ]
        )


@route
def player_succeed(state: State) -> Page:
    if len(state.player_card_hand) == 1:
        return Page(state, ["You win!"])
    else:
        state.player_card_hand.pop(0)
        return start_game_round(state)



def gen_player_hand():
    hand = []
    for num in range(26):
        hand.append(Card(randint(0, 13)))
    return hand


def gen_dealer_hand():
    hand = []
    for num in range(26):
        hand.append(Card(randint(0, 13)))
    return hand




royalty = Rules("Crowns", "A king placed on top of a queen, type 'Crowns'", False, "13", "12")
s_and_s = Rules("67!!", "A 7 placed on top of a 6, type '67!!'", False, "7", "6")
goodbye = Rules("Goodbye!", "A King placed on top of an Ace, type 'Goodbye!'", False, "13", "1")
hello = Rules("Hello!", "An Ace placed on top of a King, type 'Hello!'", False, "1", "13")
s_and_n = Rules("Funny Number", "A 6 placed on top of a 9, type 'Funny Number'", False, "6", "9")
two_twos = Rules("TuTu", "A 2 placed on top of a 2, type 'TuTu'", False, "2", "2")
unlucky = Rules("Unlucky :(", "A 4 placed on top of a King, type 'Unlucky :('", False, "4", "13")
lucky = Rules("Clover", "An 8 and a 7 placed together, type 'Clover'", False, "8", "7")
wish = Rules("Shooting Star", "Two jacks placed together, type 'Shooting Star'", False, "11", "11")
nineeleven = Rules("Towers", "A jack placed on top of a nine, type 'Towers'", False, "11", "9")
twenty_one = Rules("21-", "A 2 placed on top of a 1, type '21-'", False, "2", "1")
twenty_four = Rules("HAPPY BIRF!", "A 4 placed on a 2, type 'HAPPY BIRF!'", False, "4", "2")
eighteen = Rules("HAPPY BIRF! #2", "A 8 placed on a 1, type 'HAPPY BIRF! #2'", False, "8", "1")
king_queen = Rules("Slay Queen <3", "A queen placed on top of a king, Slay Queen <3'", False, "12", "13")
sixtysix = Rules("Don't add more", "A 6 placed on top of a 6, type 'Don't add more'", False, "6", "6")
eightyone = Rules("8111-", "A 1 placed on top of a 8, type '8111-'", False, "1", "8")
fake_mad = Rules("Ughh", "Anytime a 7 is placed on top of any card, type ' Ughh'", False, "7", "1,2,3,4,5,6,7,8,9,10,11,12,13")
sixtyfive = Rules("What about me?", "A 5 is placed on top of a 6, type 'What about me?'", False, "5", "6")
aceingthis = Rules("Ace of traits", "Anytime an Ace is placed on top of any card, type 'Ace of traits'", False, "1", "1,2,3,4,5,6,7,8,9,10,11,12,13")
count_down = Rules("Step back son", "A card placed on top of a card of one lower value, type 'Step back son'", False, "2,3,4,5,6,7,8,9,10,11,12,13", "1,2,3,4,5,6,7,8,9,10,11,12")
twins = Rules("TWINS!", "A card placed on top of itself, type 'TWINS!'", False, "1,2,3,4,5,6,7,8,9,10,11,12,13", "1,2,3,4,5,6,7,8,9,10,11,12,13")


start_server(State(
    20,
    [royalty, s_and_s, goodbye, hello, s_and_n, two_twos, unlucky, lucky, wish, nineeleven,
     twenty_one, twenty_four, eighteen, king_queen, sixtysix, eightyone, fake_mad,
     sixtyfive, aceingthis, count_down, twins],
    "1",
    [],
    []
))

