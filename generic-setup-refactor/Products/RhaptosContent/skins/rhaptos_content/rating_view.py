## Script (Python) "rating_view.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=View script for 5-star ratings

request = context.REQUEST

rating = getattr(context, 'rating', None)
if rating:
    ratedict = {}
    rating = round(rating())
    ratedict['rating'] = rating
    ratedict['count'] = context.numberOfRatings()
    ratedict['can_rate'] = request.AUTHENTICATED_USER.has_permission('Rate Module', context) and 1 or 0
    
    starslist = []
    i = 1
    stars = context.prepare_rating_for_ui(context.rating())
    for star in stars:
        starinfo = {}
        value = i
        starinfo['value'] = value
        starinfo['value_label'] = context.get_rating_value_label(value)
        starinfo['selected'] = star
        i += 1
        starslist.append(starinfo)
    ratedict['stars'] = starslist
    
    return ratedict