#ifndef __Body_h__
#define __Body_h__

//C++ libraries

//my libraries
#include "Vector3D.h"

//declarations of functions or classes 
//that are implmented in the .cxx of this folder

//class Vector3D;

class Body {

public:
  //public methods
  Body();

  //now we need a constructor that takes as arguments the three values
  //we use the method described above, which is faster
  Body(const std::string& name, double mass, const Vector3D& x, const Vector3D& v);   

  //destructors
    ~Body();
      
  //setters
  void SetName(const std::string& name);
  void SetMass(double mass);
  void SetX(const Vector3D& x);
  void SetV(const Vector3D& v);

  //getters
  std::string GetName() const;
  double GetMass() const;
  Vector3D GetX() const;
  Vector3D GetV() const;

  //others
  void Print();
  void Evolve(double dt, const Vector3D& a);
  //dt - time interval, a acceleration made of ax, ay, az

  //public members
  //none

private:
  //private methods
  //none

  //private members
  std::string m_name;
  double m_mass;
  Vector3D m_x; //position (made of x, y, z)
  Vector3D m_v; //velocity (made of vx,vy,vz)

};//end class

bool compare_by_name(const Body& left, const Body& right);
bool compare_by_mass(const Body& left, const Body& right);

#endif
