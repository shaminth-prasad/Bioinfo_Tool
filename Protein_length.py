#this is the python script to check the residue on the user input position
def get_residue(sequence, position):
    try:
        # Convert position to integer and adjust for 0-based indexing
        index = int(position) - 1
        residue = sequence[index]
        return f"Residue at position {position} is: {residue}"
    except ValueError:
        return "Error: Position must be a whole number."
    except IndexError:
        return f"Error: Position must be between 1 and {len(sequence)}."


if __name__ == "__main__":
    protein = input("Enter protein domain sequence: ").strip().upper()
    Mut=input("Enter the mutation position:")
    Pos1=input("Enter the Domain starting position:")
    Cal=(int(Mut))-((int(Pos1))-1)
    pos = Cal
    leng = len(protein)
    print("length of the sequence is:",leng)
    print(get_residue(protein, pos))