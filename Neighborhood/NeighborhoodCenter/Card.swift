//
//  Card.swift
//  NeighborhoodCenter
//
//  Created by Jai Ghanekar on 2/20/16.
//  Copyright © 2016 Jai Ghanekar. All rights reserved.
//

import Foundation


class Card {
    var id: Int?
    var author :String?
    var upvotes :Int?
    var downvotes :Int?
    var totalvotes :Int?
    var title :String?
    var description :String?
    var reported :Bool?
    var date :String?
    
    init() {
        id = 0
        author = ""
        upvotes = 0
        downvotes = 0
        totalvotes = 0
        title = ""
        description = ""
        reported = false
        date = ""
        
    }
    
    convenience init( _ dictionary:Dictionary<String, AnyObject>) {
        self.init()
        id = dictionary["id"] as? Int
        author = dictionary["author"] as? String
        upvotes = dictionary["upvotes"] as? Int
        downvotes = dictionary["downvotes"] as? Int
        totalvotes = dictionary["totalvotes"] as? Int
        title = dictionary["title"] as? String
        description = dictionary["description"] as? String
        reported = dictionary["reported"] as? Bool
        date = dictionary["date"] as? String
        
        
        
    }
    
}