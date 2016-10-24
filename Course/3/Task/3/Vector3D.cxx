#include "Vector3D.h"

//constructors

Vector3D::Vector3D()
  :x_(0.0),y_(0.0),z_(0.0)
{
}

//Vector3D::Vector3D(double x, double y, double z)
//{
//  x_=x;
//  y_=y;
//  z_=z;
//}
//but it's more memory efficien this way:
Vector3D::Vector3D(double x, double y, double z)
  :x_(x),y_(y),z_(z)
{
}

//the copy constructor
Vector3D::Vector3D(const Vector3D& v)
{
  x_=v.GetX();
  y_=v.GetY();
  z_=v.GetZ();
}

//destructor
Vector3D::~Vector3D()
{
}

//setters

void Vector3D::SetX(double x)
{
  x_=x;
}

void Vector3D::SetY(double y)
{
  y_=y;
}

void Vector3D::SetZ(double z)
{
  z_=z;
}

void Vector3D::SetXYZ(double x, double y, double z)
{
  x_=x;
  y_=y;
  z_=z;
}

//getters
double Vector3D::GetX() const
{
  return x_;
}

double Vector3D::GetY() const
{
  return y_;
}

double Vector3D::GetZ() const
{
  return z_;
}

double Vector3D::GetModule() const
{
  return sqrt(x_*x_+y_*y_+z_*z_);
}

//overloading streaming << operator for our class
//it is defined outside of the class, that's why it is not Vector3D::operator<<, but simply operator<<
std::ostream& operator<<(std::ostream& os, const Vector3D& rhs)
{
  os <<" x="<<rhs.GetX()<<" y="<<rhs.GetY()
     <<" z="<<rhs.GetZ()<<" module="<<rhs.GetModule();
  //since it is friend, it can access the private members directly, as if they were private, like this
  //os <<" x="<<v.x_<<" y="<<v.y_<<" z="<<v.GetZ()<<" module="<<v.GetModule();
  return os;
}

//for operators read here:
//http://courses.cms.caltech.edu/cs11/material/cpp/donnie/cpp-ops.html

//overload assignement operator
Vector3D& Vector3D::operator=(const Vector3D& rhs) 
{
  //Step 1: check for self-assignement:
  //we should not be allowed to do v=v;

  //this = is a pointer to the object being called
  //&rhs = is a pointer to the object being passed in as the argument

  // Check for self-assignment!
  if (this == &rhs)      // Same object?
    return *this;        // Yes, so skip assignment, and just return *this.
  
  //... // Deallocate, allocate new space, copy values...
  x_=rhs.GetX();
  y_=rhs.GetY();
  z_=rhs.GetZ();

  //return
  return *this;
}

Vector3D& Vector3D::operator+=(const Vector3D& rhs)
{
  x_+=rhs.GetX();
  y_+=rhs.GetY();
  z_+=rhs.GetZ();
  return *this;
}

Vector3D& Vector3D::operator-=(const Vector3D& rhs)
{
  x_-=rhs.GetX();
  y_-=rhs.GetY();
  z_-=rhs.GetZ();
  return *this;
}

Vector3D& Vector3D::operator*=(double rhs)
{
  x_*=rhs;
  y_*=rhs;
  z_*=rhs;
  return *this;
}

const Vector3D Vector3D::operator+(const Vector3D& rhs) const
{
  //declare a new object of type Vector3D called result
  //and initialize it to the value of the left hand side vector (*this)
  //using the assignement operator defined above
  //this has the same effect of Vector3D result(*this);
  Vector3D result=*this;
  //use the compound assignment operator to add the right hand side value to the left hand side value (result)
  result+=rhs;
  //all done, so returning the new object result
  return result;
  //in fact, we wrote three lines to write explicitely all the steps, but we could also write just one line
  //return Vector3D(*this)+=rhs;
  //This creates an unnamed instance of Vector3D, which is a copy of *this. Then, the += operator is called on the temporary value, and then returns it. 
}

const Vector3D Vector3D::operator-(const Vector3D& rhs) const
{
  Vector3D result=*this;
  result-=rhs;
  return result;
}

const Vector3D Vector3D::operator*(double rhs) const
{
  Vector3D result=*this;
  result*=rhs;
  return result;
}

//scalar product
double Vector3D::operator*(const Vector3D& rhs) const
{
  return (this->GetX()*rhs.GetX()+this->GetY()*rhs.GetY()+this->GetZ()*rhs.GetZ());
}

//vectorial product
const Vector3D Vector3D::operator^(const Vector3D& rhs) const
{
  Vector3D result;
  result.SetX(this->GetY()*rhs.GetZ()-rhs.GetZ()*rhs.GetY());
  result.SetY(this->GetZ()*rhs.GetX()-this->GetX()*rhs.GetZ());
  result.SetZ(this->GetX()*rhs.GetY()-this->GetY()*rhs.GetX());
  return result;
}



bool Vector3D::operator==(const Vector3D& rhs) const
{
  bool result;
  double comparison=0.0000001;
  //we can not compare double numbers using == due to rounding errors may seem them be different
  //so we consider they are equal if their absolute difference is smaller tan some very small number
  bool x_the_same = fabs(this->GetX()-rhs.GetX())<comparison;
  bool y_the_same = fabs(this->GetY()-rhs.GetY())<comparison;
  bool z_the_same = fabs(this->GetZ()-rhs.GetZ())<comparison;
  result= x_the_same && y_the_same && z_the_same;
  return result;
}

bool Vector3D::operator!=(const Vector3D& rhs) const
{
  return !(*this==rhs);
}
