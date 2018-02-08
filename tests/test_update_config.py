import pytest

from update.update import update_config

@pytest.fixture
def example_description(tmpdir):

  c = """saige1:

  plink_binary_prefix_pruned:
    type: file_prefix
    description: "Path to pruned plink files.
Path to plink file to be used for calculating elements of the genetic relationship matrix (GRM)."
    required: True
    default: /mnt/scratch/hunt24chunks/genotyped_pruned

  center_variables:
    type: list
    description: "List of covariates to be centered around the mean."
    required: False
    example:
      "- birthYear
       - X"

  id_column:
    type: string
    description: "Column name for the sample IDs in
          the phenotype file e.g. 'IID'"
    required: False
    default: IID

  number_of_markers:
    type: integer
    required: False
    description: "integer (>0). Number of markers to be used for estimating
          the variance ratio."
    default: 30

  skip_model_fitting:
    type: bool
    required: False
    description: Whether to skip fitting the null model and only calculating the variance ratio
    default: False"""

  f = tmpdir.mkdir("1").join("hello.txt")
  f.write(c)

  return str(f)

@pytest.fixture
def example_config(tmpdir):

    c = """# -----------
# Saige Step1
# -----------
#
# Path to pruned plink files. Path to plink file to be used for calculating
# elements of the genetic relationship matrix (GRM).
# (Required)
plink_binary_prefix_pruned: tests/test_data/saige_example/duplicated

# List of covariates to be centered around the mean.
# (Not required)
center_variables:

# Column name for the sample IDs in the phenotype file e.g. 'IID'
# (Not required)
id_column: IID

# integer (>0). Number of markers to be used for estimating the variance ratio.
# (Not required)
number_of_markers: 30

# Whether to skip fitting the null model and only calculating the variance ratio
# (Not required)
skip_model_fitting: False
"""

    f = tmpdir.mkdir("sub1").join("2")
    f.write(c)

    return str(f)

def test_update_config(example_config, example_description):

    result = update_config(example_config, example_description)

    print(result)

    assert 0
