//
//  CardViewController.swift
//  NeighborhoodCenter
//
//  Created by Jai Ghanekar on 2/20/16.
//  Copyright © 2016 Jai Ghanekar. All rights reserved.
//

import UIKit
import SwiftyJSON
import Alamofire


class CardViewController:  UIViewController, UITableViewDelegate, UITableViewDataSource {
    
    @IBOutlet weak var tableViewCell: UITableView!
    @IBOutlet weak var tableView: UITableView!
    var cardList = [Card]()
    
    

    override func viewDidAppear(animated: Bool) {
        super.viewWillAppear(animated)
        self.tableView.tableFooterView = UIView() //get rid of trailing

        
    }
    
    override func viewDidLoad() {
        
        NSOperationQueue.mainQueue().addOperationWithBlock() { () in
            self.fill_cards(OnSuccess: { source in
                
                self.cardList = source
                self.tableView.reloadData()
                
            })

            
        }
        
    }
    
    func fill_cards(OnSuccess onSuccess: ([Card]) -> Void) -> Void {
        let url = NSURL(string:"http://ec2-54-205-62-147.compute-1.amazonaws.com:8000/api/v1/cards/")
        let task = NSURLSession.sharedSession().dataTaskWithURL(url!) {(data, response, error) in
            let json = JSON(data:data!)
            var id: Int = 0
            var upvotes: Int = 0
            var downvotes: Int = 0
            var totalvotes : Int = 0
            var title: String = ""
            var description: String = ""
 
            var list = [Card]()
            
            for elements in 0...json["cards"].count - 1 {
                
                for (key,subJson):(String, JSON) in json["cards"][elements] {
                    
                    switch key {
                    case "id":
                        id = subJson.int!
                    case "upvotes":
                        upvotes = subJson.int!
                    case "downvotes":
                        downvotes = subJson.int!
                    case "totalvotes":
                        totalvotes = subJson.int!
                    case "title":
                        title = subJson.stringValue
                    case "description":
                        description = subJson.stringValue
    
                        
                        
                    default:
                         id = 0
                         upvotes = 0
                         downvotes = 0
                         totalvotes = 0
                         title = ""
                         description = ""
                    }
                    
                   
                    
                }
                let card = Card(["id":id,"upvotes":upvotes, "downvotes":downvotes, "totalvotes":totalvotes, "title":title, "desription":description])
                list.append(card)
                
            }
            
            onSuccess(list)
        }
        
        task.resume()
        
    
        
    }

    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.cardList.count
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        var mycell = tableView.dequeueReusableCellWithIdentifier("genericCell")
        if mycell == nil {
            mycell = UITableViewCell(style: .Default, reuseIdentifier: "genericCell")
        }
        mycell!.textLabel!.text = self.cardList[indexPath.row].title
        
        return mycell!
    }
    func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        
    }
    
    
}

