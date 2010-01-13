## Script (Python) "prepare_rating_for_ui"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=rating, fraction_steps=2, max_rating=5
##title=Convert rating into a format usable by module_export_template

fraction = math.modf(round(rating * fraction_steps) / fraction_steps*1.0)[0] 

result = []
for num in range(0, max_rating):
    if (rating > num) and (rating < num+1):
        # Fraction
        if fraction:
            result.append('%.1f' % fraction)
        else:
            if round(rating) < rating:
                result.append('0')
            else:
                result.append('1')
    elif rating > num:
        result.append('1')
    else:
        result.append('0')

return result
