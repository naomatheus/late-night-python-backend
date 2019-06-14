router.post('/:place_id/comment', async (req, res, next) => {
	try{
		console.log('===========================');
		console.log('HITTING POST ROUTE RESTAURANT/PLACE_ID/COMMENT');
		console.log('===========================');
		let theRestaurant;
		let theComment;
		const foundRestaurant = await Restaurant.findOne({place_id: req.params.place_id});
		console.log("Found Restaurant: ", foundRestaurant);
		///find mongoDB entry after created and populate with/comments
		const restaurantId = await Restaurant.findOne({place_id: req.params.place_id});
		///get place_id from mongoDB and store it in restaurantId variable

		if (!foundRestaurant) {

			///create mongoDB entry when route is hit if no restaurant found
			const createdRestaurant = await Restaurant.create({

				name: req.body.name,
				address: req.body.address,
				place_id: req.params.place_id

			})
			theRestaurant = createdRestaurant;
			console.log("Created Restaurant: ", createdRestaurant);
			console.log('======================================================');
			console.log(`${createdRestaurant} <==== createdRestaurant in GET'/restaurant/:place_id ROUTE`);
			console.log('======================================================');
/*else*/
		} else if (foundRestaurant) {

			theRestaurant = foundRestaurant;
			const createdComment = await Comment.create({

					commentBody: req.body.commentBody,
					commentAuthor: req.body.commentAuthor

				})
			console.log("foundRestaurant updated with new comments");
			console.log(theRestaurant);
			theRestaurant.comments.push(createdComment);
			await theRestaurant.save();
			theComment = createdComment;
			console.log('=========var theRestaurant saved======');
		}

	if (req.params.place_id === theRestaurant.place_id){
			////// if place_id === mongoDB place_id//////
			///then log the following to console...///

			console.log('======HITTING THIS BLOCK?!?!=========');
			JSON.stringify(theRestaurant);
			res.status(200).json({
					restaurant: theRestaurant, newComment: theComment
			})
			console.log('theRestaurant: ', theRestaurant, 'has been updated with comment: ', theComment);
				/// and stringify/ send res.json...

		} else {
			if(!restaurantId){
				console.log('=======================');
				console.log('no restaurant ID found!');
				console.log('=======================');
			}
		}
	}catch(err) {
		next(err);
		console.error(err);
		console.log(err);
	}
});