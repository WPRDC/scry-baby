from sources import Source, ProfilesSource

#
# The List of sources used in the source
#
# add your sources here
#
ACTIVE_SOURCES: list[Source] = [
    ProfilesSource('/indicator'),
    ProfilesSource('/data-viz'),
]
