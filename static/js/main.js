const FILLED_IN_STAR = '&#x2605'
const EMPTY_STAR = '&#x2606'

function pluralize(num, singular, plural) {
    if (plural === undefined) {
        plural = singular + 's'
    }
}
$('.toggle-like-form').on('submit', function(event) {
    event.preventDefault()
    const csrfToken = $(event.target).find('[name=csrfmiddlewaretoken]').val()
    console.log('toggling like ' + event.target.action)
    $.ajax({
        method: 'POST',
        url: event.target.action,
        success: function(results) {
            $(event.target).find('button[type=submit]').html(results.favorite ? FILLED_IN_STAR : EMPTY_STAR)

            $(`#post-${results.post_id}`).find('.post-num-favorites').text(`Liked ${results.num_of_likes} time${results.num_of_favorites !== 1 && 's'}`
            )
        }
    })
})