import csv
from math import e
import sys

from util import node, StackFrontier, QueueFrontier

names={}

people={}

movies={}

def load_data(directory):
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])        
    with open(f"{directory}/movies.csv",encoding="utf-8") as f:
        reader=csv.DictReader(f)
        for row in reader:
            movies[row['id']]={
                'title':row['title'],
                'year':row['year'],
                'stars': set()
                }


    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader=csv.DictReader(f)
        for row in reader:
            try:
                people[row['person_id']]['movies'].add(row['movie_id'])
                movies[row['movie_id']]['stars'].add(row["person_id"])
            except KeyError:
                pass



def main():
    if len(sys.argv)>2:
        sys.exit("Usage: python Degree_Checker.py [directory]")
    directory=sys.argv[1] if len(sys.argv)==2 else 'large'

    print("Data is loading.........")
    load_data(directory)
    print('data Loaded.......')

    source=person_id_for_name(input("Name : "))
    if source is None:
        sys.exit("person not found.")
    target=person_id_for_name(input("Name : "))
    if source is None:
        sys.exit("person not found.")

    path=shortest_path(source,target)

    if path is None:
        print('path is not connected.')
    else:
        degrees=len(path)
        print(f'{degrees} degrees of seperation.')
        path=[(None,source)]+path
        for i in range(degrees):
            person1=people[path[i][1]]['name']
            person2=people[path[i+1][1]]['name']
            movie=movies[path[i+1][0]]['title']
            print(f'{i+1}: {person1} and {person2} starred in {movie}')

def shortest_path(source, target):
    frontier = QueueFrontier()
    frontier.add(node(state=source, parent=None, action=None))
    explored = set()

    while not frontier.empty():
        node_ = frontier.remove()

        if node_.state == target:
            path = []
            while node_.parent is not None:
                path.append((node_.action, node_.state))
                node_ = node_.parent
            path.reverse()
            return path
        explored.add(node_.state)

        for movie_id, person_id in neighbors_for_person(node_.state):
            if not frontier.contains_state(person_id) and person_id not in explored:
                child = node(state=person_id, parent=node_, action=movie_id)
                frontier.add(child)

    return None

def person_id_for_name(name):
    person_ids=list(names.get(name.lower(),set()))
    if len(person_ids)==0:
        return None
    elif len(person_ids)>1:
        print(f'Which {name} ?')
        for person_id in person_ids:
            person=people[person_id]
            name=person['name']
            birth=person['birth']
            print(f'ID : {person_id}, Name : {name}, Birth : {birth}')
        try:
            person_id=input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    movie_ids=people[person_id]['movies']
    neighbors=set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]['stars']:
            neighbors.add((movie_id,person_id))
        
    return neighbors



if __name__=="__main__":
    main()

