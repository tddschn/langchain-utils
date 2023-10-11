import pyperclip
from pathlib import Path


referral_default_schools_list = ['NC State', 'Fudan University', 'UC San Diego']

referral_statement_default_relationship_with_referral = (
    f'{referral_default_schools_list[0]} alums'
)

# referral_name = 'Xinyuan Chen'
referral_statement_default_referral_name = 'Xinyuan Chen'

# additional_requirements = 'highlight his skills in python, cloud, data science, and web dev, and show that he  has Strong interpersonal skills.'
referral_statement_default_additional_requirements = 'highlight his skills in python, cloud, data science, and web dev, and show that he  has Strong interpersonal skills.'

# job_description: str = pyperclip.paste()
referral_statement_default_job_description = pyperclip.paste()

# resume_markdown_path: ~/testdir/resume/resume.md
referral_statement_default_resume_markdown_path = (
    Path.home() / 'testdir/resume/resume.md'
)

# title: 'Software Engineer'
referral_statement_default_title = 'Software Engineer'
