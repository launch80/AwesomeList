# Recipes

A recipe is one narrow, reproducible deployment path (hardware + OS + runtime + model + commands)
validated against [`schemas/recipe.schema.json`](../../schemas/recipe.schema.json).

There are no recipes yet: every step in a recipe must come from a run someone actually performed,
and `verification.tested_by` is required. To add one, copy
[`docs/recipe-template.yaml`](../../docs/recipe-template.yaml) to `catalog/recipes/<id>.yaml`.
