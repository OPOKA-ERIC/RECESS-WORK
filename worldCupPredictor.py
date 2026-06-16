print("===== FIFA WORLD CUP 2026 SIMULATOR =====")
country = input("Enter country name: ")
stage = 1

while stage <= 6:
    if stage == 1:
        round_name = "Group stage"
    elif stage == 2:
        round_name = "Round of 32"
    elif stage == 3:
        round_name = "Round of 16"
    elif stage == 4:
        round_name = "Quarter final"
    elif stage == 5:
        round_name = "Semi finals"
    else:
        round_name = "Finals"
    
    print(f"\n{country} is playing the {round_name}")
    result = input("Did they win or lose?: ").lower()

    #continue
    if result != "win" and result != "lose" and result != "draw":
        print("Invalid input. Please enter win or lose.")
        continue
    
    #pass
    if result == "draw":
        pass
    
    #break
    if result == "lose":
        print(f"{country} has been eliminated from the tournament.")
        break
    print(f"{country} advances to the next stage!")
    stage += 1

if stage == 7:
    print("\n CONGRATULATIONS!")
    print(f"{country} has won the FIFA Wolrd cup 2026!")
         