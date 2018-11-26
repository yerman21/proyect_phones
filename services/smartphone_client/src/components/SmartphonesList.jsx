import React from 'react';

const SmartphonesList = (props) => {
	return (					
				props.smartphones.map( (smartphone) => {
					return (
						<tr key={ smartphone.id }>
							<td  className="">
								{ smartphone.name }
							</td>
							<td  className="">
								{ smartphone.brand }
							</td>
							<td  className="">
								{ smartphone.price }
							</td>
							<td  className="">
								{ smartphone.color }
							</td>
							<td  className="">
								{ smartphone.quantity }
							</td>
							<td  className="">
								<a idsmartphone={ smartphone.id } className="button is-danger">
									<span className="icon has-text-danger">
  										X
									</span>
								</a>								
							</td>
						</tr>
						)
				})					
		)
};

export default SmartphonesList;