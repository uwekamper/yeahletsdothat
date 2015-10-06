              <div className="col-xs-6">
                <div className="row">

                  <div className="col-xs-11">
                    <h3>Perk-u-Lator 3000 (perk calculator)</h3>

                    <table className="table">
                      <thead>
                      <th>Title</th>
                      <th>Available</th>
                      <th>Price per Perk</th>
                      <th>Total</th>
                      </thead>
                      <tbody ng-repeat="perk in ctrl.perks | filter:{state: '!DELETED'}">
                      <tr>
                        <td>{ perk.title }</td>
                        <td>{ perk.available }</td>

                        <td>{ perk.amount|currency }&nbsp;{ ctrl.getCurrencyDisplay() }</td>
                        <td>{ perk.amount * perk.available | currency }&nbsp;{ ctrl.getCurrencyDisplay() }</td>
                      </tr>
                      </tbody>
                      <tbody>
                      <tr>
                        <td colspan="3" style="text-align: right;">Total</td>
                        <td>{ ctrl.getPerksTotal() | currency } { ctrl.getCurrencyDisplay() }</td>
                      </tr>
                      <tr>
                        <td colspan="3" style="text-align: right;">Campaign goal</td>
                        <td>{ ctrl.campaign.goal | currency }&nbsp;{ ctrl.getCurrencyDisplay() }</td>
                      </tr>
                      </tbody>

                    </table>
                  </div>
                </div>
                <div className="row">
                  <div className="col-xs-8 col-xs-offset-3">

                    <div className="alert alert-success" role="alert" ng-if="ctrl.goalIsReachable();">
                      You have enough perks to meet your campaign goal.
                    </div>

                    <div className="alert alert-danger" role="alert" ng-if="!ctrl.goalIsReachable();">
                      You do not have enough perks or your perks are not expensive enough.
                      This campaign could never reach its goal. You can either lower your goal
                      or add more perks and raise prices.
                    </div>
                  </div>
                </div>
              </div>
