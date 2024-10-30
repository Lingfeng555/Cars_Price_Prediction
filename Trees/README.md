# Trees

This folder contains implementations of tree-based classification and regression techniques, including **CART (Classification and Regression Trees)**, **Random Forests**, and **Bayesian Trees**. These models leverage decision tree logic to improve prediction accuracy and handle non-linear relationships in the dataset.

## Approach

Our goal is to approach the problem by dividing the dataset into targeted groups based on car type, as the evaluation criteria vary significantly across these categories. For example, factors that influence the valuation of electric cars differ from those relevant to combustion engines. This segmentation allows us to tailor models to each car type, enhancing the accuracy and relevance of predictions.

### Grouping Strategy:

- **Electric Cars / Plug-in Hybrid**: Evaluated by Lingfeng, focusing on battery capacity, range, and other electric-specific parameters.
- **Combustion Engine**: Managed by Martin, emphasizing fuel efficiency, emissions, and traditional engine performance metrics.
- **Hybrid (Non-Plug-in)**: Handled by Giovanni, considering a balance between electric and combustion factors.
- **Gas-Powered Vehicles**: Covered by Asier, with a focus on gas-specific parameters.