### ROUTES ###
#  get auth/logout - FINISHED
#  post auth/register - WORKS WITH ERRORS (creates user but does NOT redirect to login)
#  post auth/login - FINISHED
#  get auth/usercomments - DEVELOPMENT (INCOMPLETE)

#  get comment/restaurants/:place_id - DEVELOPMENT
#  put comment/restaurants/:place_id/edit/:comment_id - DEVELOPMENT
#  delete comment/restaurants/:place_id/:comment_id - DEVELOPMENT

#  get restaurants/nearby/ - FINISHED
#  post restaurants/:place_id/comment - DEVELOPMENT - hits route - doesn't C yet

# ///this route returns all comments made by a user's session///
# router.get('/usercomments', async (req, res, next) => {
#     try{
#         if (req.session.logged === true){

#             const foundUser = await User.findOne({userName: req.session.userName})
#             if (foundUser){
#                 const foundRestaurants = await Restaurant.find({userName: req.session.userName}).populate('comments');
#                 const foundComments = await Comment.find({commentAuthor: req.session.userName})
#                 res.json({
#                     status: 200,
#                     data: foundRestaurants, foundComments
#                 });
#             } else {
#                 res.json({
#                     status: 400,
#                     data: 'no data found'
#                 });
#             }
#         } else {
#             res.json({
#                 status: 400,
#                 data: 'no user session found'
#             })
#         }
#     }catch(err){
#         console.error(err);
#         next(err);
#     }
# });