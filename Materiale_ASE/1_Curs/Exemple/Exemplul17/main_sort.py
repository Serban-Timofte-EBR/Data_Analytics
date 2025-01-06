import numpy as np

persoane = np.array(
    [("Pop Adrian",22),("Ionescu Dan",53),("Popescu Diana",17),("Popa Ioana",17)],
    dtype=[("nume","U30"),("varsta","int32")]
)
print("Vectorul persoane:",persoane,sep="\n")

print("Sortare dupa nume:")
persoane.sort(order="nume")
print(persoane)
print("Sortare dupa varsta:")
persoane.sort(order="varsta")
print(persoane)
print("Sortare dupa varsta si nume:")
persoane.sort(order=["varsta","nume"])
print(persoane)
