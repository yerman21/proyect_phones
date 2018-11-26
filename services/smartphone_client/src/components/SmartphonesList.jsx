import React from 'react';

const SmartphonesList = (props) => {
	return (					
				props.smartphones.map( (smartphone) => {
					return (
						<tr>
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
								<a idsmartphone={ smartphone.id } class="button is-danger">
									<span class="icon has-text-danger">
  										<i class="fas fa-ban"></i>
									</span>
								</a>								
							</td>
						</tr>
						)
				})					
		)
};

export default SmartphonesList;