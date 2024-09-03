LN_LOGIN_URL: str = (
    "https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin"
)
LN_URL: str = "https://www.linkedin.com"
LN_FEED_URL: str = "https://www.linkedin.com/feed"
LN_JOB_SEARCH_URL: str = "https://www.linkedin.com/jobs/search/"
LN_JOBS_PER_PAGE: int = 25


########## JOB TYPES ##########
job_type: dict = {
    "1": {  # first job type of user preferences
        "Full-time": "&f_JT=F",
        "Part-time": "&f_JT=P",
        "Contract": "&f_JT=C",
        "Temporary": "&f_JT=T",
        "Volunteer": "&f_JT=V",
        "Intership": "&f_JT=I",
        "Other": "&f_JT=O",
    },
    "n": {  # n job type of user preferences
        "Full-time": "%2CF",
        "Part-time": "%2CP",
        "Contract": "%2CC",
        "Temporary": "%2CT",
        "Volunteer": "%2CV",
        "Intership": "%2CI",
        "Other": "%2CO",
    },
}
########## REMOTE ##########
remote: dict = {
    "1": {
        "On-site": "&f_WT=1",
        "Remote": "&f_WT=2",
        "Hybrid": "&f_WT=3",
    },
    "n": {
        "On-site": "%2C1",
        "Remote": "%2C2",
        "Hybrid": "%2C3",
    },
}
########## LOCATION ##########
location: dict = {
    "Spain": "&location=Spain&geoId=105646813",
    "Germany": "&location=Germany&geoId=101282230",
    "Netherlands": "&location=Netherlands&geoId=102890719",
    "Austria": "&location=Austria&geoId=103883259",
    "Belgium": "&location=Belgium&geoId=100565514",
    "Europe": "&location=Europe&geoId=100506914",
    "Africa": "&location=Africa&geoId=103537801",
    "Egypt": "&location=Egypt&geoId=106155005",
}
########## EXPERIENCE ##########
experience: dict = {
    "1": {
        "Internship": "&f_E=1",
        "Entry level": "&f_E=2",
        "Associate": "&f_E=3",
        "Mid-Senior level": "&f_E=4",
        "Director": "&f_E=5",
        "Executive": "&f_E=6",
    },
    "n": {
        "Internship": "%2C1",
        "Entry level": "%2C2",
        "Associate": "%2C3",
        "Mid-Senior level": "%2C4",
        "Director": "%2C5",
        "Executive": "%2C6",
    },
}
########## DATE POSTED ##########
date_posted: dict = {
    "Any Time": "",
    "Past Month": "&f_TPR=r2592000",
    "Past Week": "&f_TPR=r604800",
    "Past 24 hours": "&f_TPR=r86400",
}
########## SORT ##########
sort_by: dict = {
    "Recent": "&sortBy=DD",
    "Relevent": "&sortBy=R",
}
