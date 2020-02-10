# Apriltag creator

This repository provides code to generate PDFs of traffic signs/ localization tags using the Duckietown AprilTag database.

## How to use it

### 1. Create intersection tags
To generate sets of intersections composed by unique IDs, first generate a list containing sets of unique IDs by running:

```bash
cd code
python3 create_batches.py
```

This should create a set of `.csv` files in the folder `data/lists`

Now you need to run the main file specifying that you want a set of specific AprilTags, and the name of the set you want. For example:
```bash
python3 create_tags.py --config set --set_name 3_intersection_0
```

Do this for all different sets you want. Then go to step 5.

### 2. Create localization tags
To generate sets of localization tags composed by unique IDs, run

```bash
cd code
python3 create_batches.py --config localization
```

If you wish different settings, have a look at `data/config/pdf_specs.yaml`, for example you can change the
text printed below the tag (`id_text`)

Now go to step 5.

### 3. Create Duckiebot tags
To generate sets of vehicle-localization tags composed by unique IDs, run

```bash
cd code
python3 create_batches.py --config autobots
```

If you wish different settings, have a look at `data/config/pdf_specs.yaml`, for example you can change the
text printed below the tag (`id_text`)

Now go to step 5.

### 4. Custom settings
You can generate custom tags by passing arguments when you run `create_batches.py`, this is useful for example if 
you wish to print all possible AprilTags. Have a look at `code/utils/creator_utils.py` to check the arguments of the parser.
Keep in mind that the argument `--config`, overwrites the other arguments you pass, so in this case do not pass it.


### 5. generating the PDF
In order to generate the PDF, compile the `.tex` file that has been generated in `output/`. To do this, make sure you
have `pdflatex` installed, then in the `code` folder, run:

```bash
source compile_pdfs.sh
```
