# CEAPS Data Science Project

## Introduction

This repository is a Data Science project to analyze data about the expanses declared by Brazilian senators, divided by year, available on [CEAPS](https://www12.senado.leg.br/transparencia/dados-abertos-transparencia/dados-abertos-ceaps?utm_medium=email&_hsenc=p2ANqtz-9oraJDtmhd8_VnMw6lGWYoF-FANWSpngMwRtg5ovo9-FUTm4kwZNmhdv-VODztf3mjAuiwU6VMgVCFd_3ndX_vSNKFpg&_hsmi=231298145&utm_content=231298145&utm_source=hs_automation) (Cota para Exercício da Atividade Parlamentar dos Senadores).

## Project Structure
The project is organized as follows:

- `data/`: This directory contains raw and processed data files used in the project.
- `src/`: This directory contains source code and scripts to run separately, such as data preprocessing and model evaluation.
- `notebooks/`: This directory contains Jupyter notebooks with the data analysis and machine learning models.
- `results/`: This directory stores the output files and visualizations generated during the analysis.

## Dependencies
To run this project, you will need the dependencies in `requirements.txt`.

You can create a virtual environment in whatever way you consider most appropriate. The form applied and recommended in this project was by `venv`:

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Usage
To get started, follow these steps:

1. Clone this repository to your local machine.
2. Download the [CEAPS](https://www12.senado.leg.br/transparencia/dados-abertos-transparencia/dados-abertos-ceaps?utm_medium=email&_hsenc=p2ANqtz-9oraJDtmhd8_VnMw6lGWYoF-FANWSpngMwRtg5ovo9-FUTm4kwZNmhdv-VODztf3mjAuiwU6VMgVCFd_3ndX_vSNKFpg&_hsmi=231298145&utm_content=231298145&utm_source=hs_automation) data.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Run the [data wrangling](./src/data_wrangling.py) script to clean and format the data.
3. Navigate to the `notebooks/` directory and open the Jupyter notebooks.
4. Run the cells in the notebooks to perform data analysis and train machine learning models.
5. Visualize the results in `results/` directory.

### Observations
You might have some difficulties with the enconding of the data files. The encoding that best matches for me was `Windows-1258`. You can set it when running the data wrangling script with `--enconding Windows-1258` or you can set it to `auto` and try to identify the best one.

Moreover, there are some date records that do not match the year. Since these cases correspond to less than 1% of the rows, it was decided to remove them to maintain the feasibility of the dates.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact
If you have any questions or suggestions, please feel free to reach out to us at [this e-mail](mailto:alext.oliver24@gmail.com).
