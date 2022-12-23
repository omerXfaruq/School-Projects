%Omer Faruk Ozdemir
%2016400048
%compiling: not known
%complete: not known

:-include(pokemon_data).

%%%
% both hp goes below 0? which team wins?
% both hit each other 0?
% same pokemon fight with itself?


%%
%-When both hp goes below 0 together in a pokemon_fight, which one wins?

%* Pokemon with the higher hp.


%-When pokemons hit 0 to each other because of types, which one wins?

%* Damage = (0.5 * AttackerPokemonLevel * (AttackerPokemonAttack/DefenderPokemonDefense) * Multiplier) + 1

%In the damage formula there is a +1 outside of the paranthesis which makes Damage >= 1


%-Can a pokemon fight with itself, if it can which pokemon wins?

%* Good question. You need to write a winning condition just for the predicate 4.8 pokemon_tournament(+PokemonTrainer1, +PokemonTrainer2, -WinnerTrainerList). If there happens to be a tie like you've mentioned, then PokemonTrainer1 wins.


%%%

%4.1 find pokemon evolution(+PokemonLevel, +Pokemon, -EvolvedPokemon)


%create recursion end condition via new_find_pokemon_evolution

new_find_pokemon_evolution(PokemonLevel,Pokemon,EvolvedPokemon):-
pokemon_evolution(Pokemon,MemPokemon,X),X=<PokemonLevel,  new_find_pokemon_evolution(PokemonLevel,MemPokemon,EvolvedPokemon).
new_find_pokemon_evolution(_,Pokemon,Pokemon).

find_pokemon_evolution(PokemonLevel,Pokemon,EvolvedPokemon):-
pokemon_evolution(Pokemon,MemPokemon,X),X=<PokemonLevel, new_find_pokemon_evolution(PokemonLevel,MemPokemon,EvolvedPokemon),!.

find_pokemon_evolution(_,Pokemon,Pokemon).

%4.2 pokemon_level_stats(+PokemonLevel, ?Pokemon, -PokemonHp, -PokemonAttack,-PokemonDefense)

pokemon_level_stats(PokemonLevel, Pokemon, PokemonHp, PokemonAttack, PokemonDefense):-
pokemon_stats(Pokemon,_,Hp,Attack,Defense), 
PokemonHp is (Hp+PokemonLevel*2),PokemonAttack is (Attack+PokemonLevel),PokemonDefense is (Defense+PokemonLevel).


%need to delete last fail output.
%4.3 single type multiplier(?AttackerType, ?DefenderType, ?Multiplier)

list_traverse([Value|_],[Element|_],Element,Value).

list_traverse([_|Tail1],[_|Tail2],Element,Value):-
list_traverse(Tail1,Tail2,Element,Value),!.

single_type_multiplier(AttackerType, DefenderType, Multiplier):-
type_chart_attack(AttackerType,L1),pokemon_types(L2),list_traverse(L1,L2,DefenderType,Multiplier).



%4.4 type multiplier(?AttackerType, +DefenderTypeList, ?Multiplier)


type_multiplier(_,[],1).

type_multiplier(AttackerType,[X|DefenderTypeList],Multiplier):-
single_type_multiplier(AttackerType,X,Multi),type_multiplier(AttackerType,DefenderTypeList,Y),Multiplier is (Multi*Y).


%4.5 pokemon type multiplier(?AttackerPokemon, ?DefenderPokemon, ?Multiplier)

max(X,Y,Z):-
	X=<Y, Z is Y.

max(X,Y,Z):-
	X>Y, Z is X.

maxForAll([],_,0).

maxForAll([Head|AttackerTypes],DefenderTypes,Multiplier):-
	type_multiplier(Head,DefenderTypes,X),
	maxForAll(AttackerTypes,DefenderTypes,Y),
	max(X,Y,Multiplier).

pokemon_type_multiplier(AttackerPokemon,DefenderPokemon,Multiplier):-
	pokemon_stats(AttackerPokemon,AttackerTypes,_,_,_),
	pokemon_stats(DefenderPokemon,DefenderTypes,_,_,_),
	maxForAll(AttackerTypes,DefenderTypes,Multiplier).


%4.6 pokemon attack(+AttackerPokemon, +AttackerPokemonLevel, +DefenderPokemon,+DefenderPokemonLevel, -Damage)


pokemon_attack(AttackerPokemon, AttackerPokemonLevel, DefenderPokemon,DefenderPokemonLevel, Damage):-
	pokemon_level_stats(AttackerPokemonLevel,AttackerPokemon,_,AttackerPokemonAttack,_),
	pokemon_level_stats(DefenderPokemonLevel,DefenderPokemon,_,_,DefenderPokemonDefense),
	pokemon_type_multiplier(AttackerPokemon,DefenderPokemon,Multiplier),
	Damage is ((0.5*AttackerPokemonLevel * (AttackerPokemonAttack / DefenderPokemonDefense)* Multiplier )+1).

	
	
%4.7 pokemon_fight(+Pokemon1, +Pokemon1Level, +Pokemon2, +Pokemon2Level,-Pokemon1Hp, -Pokemon2Hp, -Rounds)

intermediate_predicate(_, _, _, _,Pokemon1Hp, Pokemon2Hp, Pokemon1HpOld, Pokemon2HpOld, Rounds):-
	Pokemon1HpOld=<0,
	Pokemon1Hp is Pokemon1HpOld,
	Pokemon2Hp is Pokemon2HpOld,
	Rounds=0,!.

intermediate_predicate(_, _, _, _,Pokemon1Hp, Pokemon2Hp, Pokemon1HpOld, Pokemon2HpOld, Rounds):-
	Pokemon2HpOld=<0,
	Pokemon1Hp is Pokemon1HpOld,
	Pokemon2Hp is Pokemon2HpOld,
	Rounds=0,!.
	
intermediate_predicate(Pokemon1, Pokemon1Level, Pokemon2, Pokemon2Level,Pokemon1Hp, Pokemon2Hp, Pokemon1HpOld, Pokemon2HpOld, Round	):-
	pokemon_attack(Pokemon1,Pokemon1Level,Pokemon2,Pokemon2Level,Damage1), 
	pokemon_attack(Pokemon2,Pokemon2Level,Pokemon1,Pokemon1Level,Damage2),
	intermediate_predicate(Pokemon1,Pokemon1Level,Pokemon2,Pokemon2Level,Pokemon1Hp,Pokemon2Hp, (Pokemon1HpOld-Damage2) ,(Pokemon2HpOld-Damage1),Rounds),
	Round is (Rounds+1).

pokemon_fight(Pokemon1, Pokemon1Level, Pokemon2, Pokemon2Level,Pokemon1Hp, Pokemon2Hp, Rounds):-
	pokemon_level_stats(Pokemon1Level, Pokemon1, Pokemon1HpMax, _,_),
	pokemon_level_stats(Pokemon2Level, Pokemon2, Pokemon2HpMax, _,_),
	intermediate_predicate(Pokemon1, Pokemon1Level, Pokemon2, Pokemon2Level,Pokemon1Hp, Pokemon2Hp,Pokemon1HpMax,Pokemon2HpMax, Rounds).

	


%4.8 pokemon_tournament(+PokemonTrainer1, +PokemonTrainer2, -WinnerTrainerList)

%%%

pokemon_tournament(PokemonTrainer1,PokemonTrainer2, WinnerTrainerList):-
	pokemon_trainer(PokemonTrainer1,PokemonList1,LevelList1),
	pokemon_trainer(PokemonTrainer2,PokemonList2,LevelList2),
	fight_chain(PokemonTrainer1,PokemonTrainer2,PokemonList1,LevelList1,PokemonList2,LevelList2,WinnerTrainerList).

%fight_chain does all the work.

fight_chain(_,_,[],[],[],[],[]).	
	
fight_chain(PokemonTrainer1,PokemonTrainer2,[Pokemon1|PokemonList1],[Level1|LevelList1],[Pokemon2|PokemonList2],[Level2|LevelList2],[WinnerTeam|WinnerTrainerList]):-
	find_pokemon_evolution(Level1,Pokemon1,EvolvedPokemon1),
	find_pokemon_evolution(Level2,Pokemon2,EvolvedPokemon2),
	fight_winner(EvolvedPokemon1,Level1,EvolvedPokemon2,Level2,WinnerTeamNumber),
	returnTeam(WinnerTeamNumber,PokemonTrainer1,PokemonTrainer2,WinnerTeam),
	fight_chain(PokemonTrainer1,PokemonTrainer2,PokemonList1,LevelList1,PokemonList2,LevelList2,WinnerTrainerList).
	
%return team according to number
returnTeam(1,Team1,_,Team1).

returnTeam(2,_,Team2,Team2).


%fight_winner(+Pokemon1,+Pokemon2,WinnerNumber)


	
fight_winner(Pokemon1,Pokemon1Level,Pokemon2,Pokemon2Level,1):-
	pokemon_fight(Pokemon1,Pokemon1Level,Pokemon2,Pokemon2Level,Pokemon1Hp,_,_),
	Pokemon1Hp>0,!.
fight_winner(Pokemon1,Pokemon1Level,Pokemon2,Pokemon2Level,2):-
	pokemon_fight(Pokemon1,Pokemon1Level,Pokemon2,Pokemon2Level,_,Pokemon2Hp,_),
	Pokemon2Hp>0 ,!.


fight_winner(Pokemon1,Pokemon1Level,Pokemon2,Pokemon2Level,1):-
	pokemon_fight(Pokemon1,Pokemon1Level,Pokemon2,Pokemon2Level,Pokemon1Hp,_,_),
	Pokemon1Hp>Pokemon2Hp,!.
	

fight_winner(Pokemon1,Pokemon1Level,Pokemon2,Pokemon2Level,2):-
	pokemon_fight(Pokemon1,Pokemon1Level,Pokemon2,Pokemon2Level,Pokemon1Hp,_,_),
	Pokemon1Hp<Pokemon2Hp,!.
	
fight_winner(Pokemon1,Pokemon1Level,Pokemon2,Pokemon2Level,1):-
	pokemon_fight(Pokemon1,Pokemon1Level,Pokemon2,Pokemon2Level,Pokemon1Hp,_,_),
	Pokemon1Hp=Pokemon2Hp,!.
	
	

		
	
	
%4.9 best pokemon(+EnemyPokemon, +LevelCap, -RemainingHP, -BestPokemon)
%%%
	
%Finds max value and which pokemon's is it
edited_max(Value1,Value2,ValueOut,Pokemon1,Pokemon2,Pokemon2):-
	max(Value1,Value2,ValueOut),
	Value2=ValueOut.
	
edited_max(Value1,Value2,ValueOut,Pokemon1,Pokemon2,Pokemon1):-
	max(Value1,Value2,ValueOut),
	Value1=ValueOut .
	
%Finds the best pokemon against enemyPokemon	
getMaxAgainst(EnemyPokemon,[LastPokemon],LastMaxPokemon,MaxPokemon,LevelCap,LastMaxHp,FinalMaxHp):-
	pokemon_fight(EnemyPokemon, LevelCap, LastPokemon, LevelCap,_, Pokemon2Hp, _),
	edited_max(LastMaxHp,Pokemon2Hp,FinalMaxHp,LastMaxPokemon,LastPokemon,MaxPokemon).

getMaxAgainst(EnemyPokemon,[LastPokemon|PokemonList],LastMaxPokemon,MaxPokemon,LevelCap,LastMaxHp,FinalMaxHp):-
	pokemon_fight(EnemyPokemon, LevelCap, LastPokemon, LevelCap,_, Pokemon2Hp, _),
	edited_max(LastMaxHp,Pokemon2Hp,CurrentMaxHp,LastMaxPokemon,LastPokemon,CurrentMaxPokemon),
	getMaxAgainst(EnemyPokemon,PokemonList,CurrentMaxPokemon,MaxPokemon,LevelCap,CurrentMaxHp,FinalMaxHp).


best_pokemon(EnemyPokemon, LevelCap, RemainingHP, BestPokemon):-
	findall(Pokemon,pokemon_stats(Pokemon,_,_,_,_),PokemonList),
	getMaxAgainst(EnemyPokemon, PokemonList,EnemyPokemon,BestPokemon,LevelCap,0,RemainingHP).
	
	

	
		
%4.10 best_pokemon_team(+OpponentTrainer, -PokemonTeam)

create_pokemon_team([],[],[]).


create_pokemon_team([Pokemon1|Team1],[Level|LevelList],[Pokemon2|Team2]):-
	best_pokemon(Pokemon1,Level,_,Pokemon2),
	create_pokemon_team(Team1,LevelList,Team2).

best_pokemon_team(OpponentTrainer, PokemonTeam):-
	pokemon_trainer(OpponentTrainer,PokemonList1,LevelList1),
	create_pokemon_team(PokemonList1,LevelList1,PokemonTeam).
	
	
%4.11 pokemon types(+TypeList, ?InitialPokemonList, -PokemonList)


%list_contains(+Element,+List,0)
%Returns true if element is in the list.

list_contains(_,_,1):-
	!.

list_contains(Element,[Head|List],0):-
	Element=Head,!.
	
list_contains(Element,[Head|List],0):-
	list_contains(Element,List,0),!.
	
	
	
%pokemon_is_typeOf(+Pokemon,+TypeList, 0)
%Returns true if pokemon is a type from TypeList.

pokemon_is_typeOf(_,_,1):-
	!.

pokemon_is_typeOf(Pokemon,[Head|TypeList],0):-
	pokemon_stats(Pokemon, PokemonTypes, _, _, _),
	list_contains(Head,PokemonTypes,0),!.


pokemon_is_typeOf(Pokemon,[Head|TypeList],0):-
	pokemon_is_typeOf(Pokemon,TypeList,0),!.


%pokemon_types(+TypeList, ?InitialPokemonList, -PokemonList)

pokemon_types(_, [], []).

pokemon_types(TypeList,[Pokemon|InitialPokemonList],[Pokemon|PokemonList]):-
	pokemon_is_typeOf(Pokemon,TypeList,0),
	pokemon_types(TypeList,InitialPokemonList,PokemonList),!.

pokemon_types(TypeList,[Pokemon|InitialPokemonList],PokemonList):-
	pokemon_types(TypeList,InitialPokemonList,PokemonList),!.
	
	
%4.12 generate pokemon team(+LikedTypes, +DislikedTypes, +Criterion, +Count,-PokemonTeam)

%works in a inverse way of pokemon_types
%not_liked_pokemon_types(+TypeList,?InitialPokemonList, -PokemonList)

not_liked_pokemon_types(_,[], []).


not_liked_pokemon_types(TypeList,[Pokemon|InitialPokemonList],PokemonList):-
	pokemon_is_typeOf(Pokemon,TypeList,0),
	pokemon_types(TypeList,InitialPokemonList,PokemonList),!.

not_liked_pokemon_types(TypeList,[Pokemon|InitialPokemonList],[Pokemon|PokemonList]):-
	pokemon_types(TypeList,InitialPokemonList,PokemonList),!.



%Does not work correctly
%Need update for sort, and design	
%generate pokemon team(+LikedTypes, +DislikedTypes, +Criterion, +Count,-PokemonTeam)

generate_pokemon_team(LikedTypes, DislikedTypes, Criterion, Count,PokemonTeam):-
	findall(Pokemon,pokemon_stats(Pokemon,_,_,_,_),PokemonList),
	pokemon_types(LikedTypes,PokemonList,LikedPokemonList),
	not_liked_pokemon_types(DislikedTypes,LikedPokemonList,PokemonTeam).


