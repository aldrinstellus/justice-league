import React from "react";
import { Card, Input, Badge, Avatar, Checkbox } from "@/components/ui";

export interface Dashboard10Props {
  className?: string;
}

export function Dashboard10({ className }: Dashboard10Props) {
  return (
    <div className="`flex flex-col gap-4 ${className}`">
  <Card className="p-4 space-y-2">
    <Card className="p-4 space-y-2">
      <div className="space-y-2">
        <div className="space-y-2">
          <p className="text-sm">Announcement</p>
          <p className="text-sm">View all</p>
        </div>
        <div className="space-y-2">
          <Card className="p-4 space-y-2">
            <div className="space-y-2">
            </div>
            <div className="space-y-2">
            </div>
          </Card>
        </div>
      </div>
      <div className="space-y-2">
        <div className="space-y-2">
          <p className="text-sm">Upcoming Tests</p>
          <p className="text-sm">View all</p>
        </div>
        <Card className="p-4 space-y-2">
          <div className="space-y-2">
            <Card className="p-4 space-y-2">
            </Card>
          </div>
          <div className="space-y-2">
          </div>
          <div className="space-y-2">
          </div>
        </Card>
      </div>
      <div className="space-y-2">
        <div className="space-y-2">
          <p className="text-sm">To-Do List</p>
          <p className="text-sm">View all</p>
        </div>
        <div className="space-y-2">
          <Card className="p-4 space-y-2">
            <Card className="p-4 space-y-2">
            </Card>
            <Card className="p-4 space-y-2">
            </Card>
            <Card className="p-4 space-y-2">
            </Card>
            <Card className="p-4 space-y-2">
            </Card>
          </Card>
          <div className="space-y-2">
          </div>
        </div>
      </div>
    </Card>
    <Card className="p-4 space-y-2">
      <div className="space-y-2">
        <div className="space-y-2">
          <p className="text-sm">Good Morning, Georgia 👋</p>
          <p className="text-sm">Nice to have you back!
Get ready and continue your lesson today.</p>
        </div>
        <div className="space-y-2">
          <Card className="p-4 space-y-2">
            <p className="text-sm">My Badges</p>
            <p className="text-sm">Today, April 22</p>
            <p className="text-sm">View all</p>
          </Card>
          <Card className="p-4 space-y-2">
            <div className="space-y-2">
            </div>
            <div className="space-y-2">
            </div>
            <div className="space-y-2">
            </div>
          </Card>
        </div>
      </div>
      <div className="space-y-2">
        <div className="space-y-2">
          <p className="text-sm">Today’s Classes</p>
          <p className="text-sm">View all</p>
        </div>
        <Card className="p-4 space-y-2">
          <Card className="p-4 space-y-2">
            <div className="space-y-2">
            </div>
          </Card>
          <Card className="p-4 space-y-2">
            <div className="space-y-2">
            </div>
          </Card>
          <Card className="p-4 space-y-2">
            <div className="space-y-2">
            </div>
          </Card>
        </Card>
      </div>
      <Card className="p-4 space-y-2">
        <div className="space-y-2">
          <p className="text-sm">Your Courses</p>
        </div>
        <Card className="p-4 space-y-2">
          <div className="space-y-2">
            <p className="text-sm">All </p>
          </div>
          <p className="text-sm">Language Arts</p>
          <p className="text-sm">Math</p>
          <p className="text-sm">Science</p>
          <p className="text-sm">History & Geography</p>
          <p className="text-sm">Spelling</p>
        </Card>
        <Card className="p-4 space-y-2">
          <Card className="p-4 space-y-2">
            <Card className="p-4 space-y-2">
            </Card>
          </Card>
          <Card className="p-4 space-y-2">
            <Card className="p-4 space-y-2">
            </Card>
          </Card>
          <Card className="p-4 space-y-2">
            <Card className="p-4 space-y-2">
            </Card>
          </Card>
        </Card>
        <div className="space-y-2">
          <Card className="p-4 space-y-2">
            <Card className="p-4 space-y-2">
            </Card>
          </Card>
          <Card className="p-4 space-y-2">
            <Card className="p-4 space-y-2">
            </Card>
          </Card>
        </div>
      </Card>
    </Card>
    <div className="space-y-2">
      <div className="space-y-2">
        <div className="space-y-2">
          <Avatar />
        </div>
        <p className="text-sm">Chat</p>
      </div>
      <Card className="p-4 space-y-2">
        <div className="space-y-2">
        </div>
      </Card>
    </div>
    <div className="space-y-2">
      <div className="space-y-2">
        <Card className="p-4 space-y-2">
          <div className="space-y-2">
          </div>
          <div className="space-y-2">
          </div>
          <div className="space-y-2">
          </div>
        </Card>
      </div>
    </div>
    <Card className="p-4 space-y-2">
      <div className="space-y-2">
        <div className="space-y-2">
          <p className="text-sm">10</p>
        </div>
      </div>
      <Card className="p-4 space-y-2">
        <div className="space-y-2">
        </div>
        <div className="space-y-2">
          <p className="text-sm">Georgia Watson</p>
          <p className="text-sm">Class 10</p>
        </div>
      </Card>
    </Card>
  </Card>
    </div>
  );
}
