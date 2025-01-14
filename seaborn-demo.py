import seaborn as sns
import matplotlib.pyplot as plt

# Load the example dataset
penguins = sns.load_dataset("penguins")

# Create a pairplot with hue for species
sns.pairplot(
    penguins,
    hue="species",  # Color by species
    diag_kind="kde",  # Use KDE plots on the diagonal
    palette="Set2",  # Nice color palette
)

# Show the plot
plt.suptitle("Penguins Dataset: Pairplot of Features", y=1.02, fontsize=16)
plt.show()


