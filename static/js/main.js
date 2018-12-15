const FILLED_IN_STAR = '&#x2605'
const EMPTY_STAR = '&#x2606'

function pluralize(num, singular, plural) {
    if (plural === undefined) {
        plural = singular + 's'
    }
    return `${num} ${num === 1 ? singular : plural}`
}

$('.toggle-favorite-form').on('submit', function(event) {
    event.preventDefault()
    let csrfToken = $(event.target).find('[name=csrfmiddlewaretoken]').val()
    $.ajax({
        method: 'POST',
        url: event.target.action,
        data: {
            'csrfmiddlewaretoken': csrfToken
        }
    }).then(function(results) {
        $(event.target).find('.fav-button').html(results.favorite ? FILLED_IN_STAR : EMPTY_STAR)
        return results
    }).then(function(results) {
        $(`#fav-${results.slug}`)
        .find('.num-favorites')
        .text(`Favorited ${pluralize(results.num_of_favorites, 'time')}`
        )        
    })
})

$('.toggle-like-form').on('submit', function(event) {
    event.preventDefault()
    let csrfToken = $(event.target).find('[name=csrfmiddlewaretoken]').val()
    $.ajax({
        method: 'POST',
        url: event.target.action,
        data: {
            'csrfmiddlewaretoken': csrfToken
        }
    }).then(function(results) {
        $(event.target).find('.like-button').html(results.like ? FILLED_IN_STAR : EMPTY_STAR)
        return results
    }).then(function(results) {
        $(`#like-${results.slug}`)
        .find('.num-likes')
        .text(`Liked ${pluralize(results.num_of_likes, 'time')}`
        )        
    })
})

$('.toggle-follow-form').on('submit', function(event) {
    event.preventDefault()
    let csrfToken = $(event.target).find('[name=csrfmiddlewaretoken]').val()
    $.ajax({
        method: 'POST',
        url: event.target.action,
        data: {
            'csrfmiddlewaretoken': csrfToken
        }
    }).then(function(results) {
        $(event.target).find('.follow-button').html(results.follow ? 'Unfollow' : 'Follow')
        return results
    })
})



//         success: function(results) {
//             $(event.target).find('button[type=submit]').html(results.favorite ? FILLED_IN_STAR : EMPTY_STAR)
//             return results
//         })
//             $(`#post-${results.post_id}`).find('.post-num-favorites').text(`Favorited ${results.num_of_favorites} time${results.num_of_favorites !== 1 && 's'}`
//             )}
//     })
// })