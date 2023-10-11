REFERRAL_STATEMENT = '''
Pretend you're {your_title} and you're referring Xinyuan Chen to the role below:

"""
{job_description}
"""

Here's {referral_name}'s resume:
"""
{resume_markdown_content}
"""

You and {referral_name} are {relationship_with_referral}, write a paragraph mentioning how he is fit for the role, it should be as if you're telling about you how {referral_name}'s fit for the role. {additional_requirements}
`.  tell a good story. Use less than 200 words.
'''.strip()
